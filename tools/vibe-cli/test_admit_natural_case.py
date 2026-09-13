#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator, FormatChecker


SCRIPT = Path(__file__).with_name("admit_natural_case.py")
ROOT = SCRIPT.parents[2]
FIXTURES = ROOT / "tests/fixtures/natural_case_admission"
SPEC = importlib.util.spec_from_file_location("admit_natural_case", SCRIPT)
assert SPEC and SPEC.loader
ADMISSION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADMISSION)
FIXED_NOW = datetime(2026, 8, 11, 6, 49, tzinfo=timezone.utc)


def _process_admit(registration: Path, request: Path, admissions: Path, output: multiprocessing.Queue) -> None:
    try:
        output.put(("ok", ADMISSION.admit(registration, request, admissions, now=FIXED_NOW)))
    except Exception as exc:  # pragma: no cover
        output.put(("error", f"{type(exc).__name__}: {exc}"))


class NaturalCaseAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.experiment_id = "2026-08-11_natural-case-admission-test"
        self.experiment = self.root / "experiments" / self.experiment_id
        self.experiment.mkdir(parents=True)
        self.registration = self.experiment / "registration.v2.json"
        registration = json.loads((ROOT / "experiments/_template/registration.v2.json").read_text(encoding="utf-8"))
        registration["experiment_id"] = self.experiment_id
        registration["registered_at"] = "2026-08-11T06:40:00Z"
        registration["natural_case_admission"] = True
        registration["consumer"]["organ"] = "Grabowski"
        registration["consumer"]["commitment"]["evidence_ref"] = "receipt:test-consumer-commitment"
        registration["consumer"]["commitment"]["confirmed_at"] = "2026-08-11T06:40:00Z"
        registration["decision_target"]["decision_ref"] = "receipt:test-decision-target"
        registration["intervention"]["name"] = "natural-case-admission-test"
        registration["measurement"]["primary_metric"] = "review_roundtrips"
        registration["consumer"]["commitment"]["valid_until"] = "2026-09-01T00:00:00Z"
        registration["decision_target"]["owner"] = "Grabowski"
        registration["control_condition"]["id"] = "live_preflight_only"
        registration["treatment_condition"]["id"] = "live_preflight_plus_history"
        registration["review_at"] = "2026-08-20T00:00:00Z"
        registration["expires_at"] = "2026-09-01T00:00:00Z"
        registration["closure"]["archive_path"] = f"experiments/_archive/{self.experiment_id}"
        self.registration.write_text(json.dumps(registration, indent=2) + "\n", encoding="utf-8")
        results = self.experiment / "results"
        results.mkdir()
        (results / "decision.yml").write_text("verdict: not_executed\n", encoding="utf-8")
        (self.experiment / "manifest.yml").write_text("experiment:\n  status: designed\n", encoding="utf-8")
        self.sync_active_registry()
        self.admissions = self.experiment / "artifacts/admissions"

    def sync_active_registry(self) -> None:
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        payload = {"schema_version":"active-experiments.v1","max_active":5,"experiments":[{"experiment_id":registration["experiment_id"],"path":f"experiments/{registration['experiment_id']}","state":"designed","consumer":registration["consumer"]["organ"],"decision_target":registration["decision_target"]["question"],"primary_metric":registration["measurement"]["primary_metric"],"review_at":registration["review_at"],"expires_at":registration["expires_at"],"source_ref":f"experiments/{registration['experiment_id']}/results/decision.yml"}]}
        (self.root / "experiments/active.v1.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def request(self, *, case_id: str = "chronik-natural-001", condition: str = "live_preflight_only") -> dict:
        value = json.loads((FIXTURES / "valid-control-request.json").read_text(encoding="utf-8"))
        value["case_id"] = case_id
        assignment_seed = f"assignment:{case_id}:{condition}"
        value["assignment"] = {
            "condition": condition,
            "assigned_by": "operator:prospective",
            "evidence_ref": f"receipt:{assignment_seed}",
            "evidence_sha256": hashlib.sha256(assignment_seed.encode()).hexdigest(),
            "recorded_before_planning": True,
        }
        return value

    def write_request(self, value: dict, name: str = "request.json") -> Path:
        path = self.root / name
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def admit(self, value: dict, *, now: datetime = FIXED_NOW) -> dict:
        return ADMISSION.admit(self.registration, self.write_request(value), self.admissions, now=now)

    def record_path(self, case_id: str = "chronik-natural-001") -> Path:
        return self.admissions / case_id / "admission.json"

    def unique_case(self, case_id: str, *, condition: str = "live_preflight_only", evidence_digit: str = "3") -> dict:
        value = self.request(case_id=case_id, condition=condition)
        value["eligibility_evidence"] = {
            "ref": f"receipt:{case_id}",
            "sha256": evidence_digit * 64,
            "captured_at": "2026-08-11T06:48:41Z",
        }
        value["triggered_by"] = f"receipt:trigger:{case_id}"
        return value

    def test_admission_freezes_explicit_assignment_and_review(self) -> None:
        result = self.admit(self.request())
        record = json.loads(self.record_path().read_text(encoding="utf-8"))
        schema = json.loads(ADMISSION.ADMISSION_SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "admitted")
        self.assertFalse(result["automatic_assignment"])
        self.assertEqual(record["registration_sha256"], ADMISSION.sha256_json(registration))
        self.assertEqual(record["assignment_evidence"]["condition"], "live_preflight_only")
        self.assertFalse(record["assignment_evidence"]["automatic"])
        self.assertEqual(record["assignment_evidence"]["mode"], "explicit_preplanning_assignment")
        self.assertEqual(record["assignment_evidence"]["fairness_claim"], "not_established_by_registration_v2")
        self.assertNotIn("sequence_index", record["assignment_evidence"])
        self.assertEqual(record["review_preparation"]["status"], "pending_independent_review")
        self.assertEqual(record["traceability"]["outcome"], "explicit_condition_assignment_sealed")
        self.assertEqual(self.record_path().stat().st_mode & 0o777, 0o444)

    def test_identical_retry_is_idempotent_and_preserves_original_bytes(self) -> None:
        request = self.request()
        first = self.admit(request)
        before = self.record_path().read_bytes()
        second = self.admit(request, now=FIXED_NOW + timedelta(hours=1))
        self.assertFalse(first["idempotent"])
        self.assertTrue(second["idempotent"])
        self.assertEqual(second["status"], "already_admitted")
        self.assertEqual(self.record_path().read_bytes(), before)

    def test_conflicting_retry_is_refused_without_mutation(self) -> None:
        request = self.request()
        self.admit(request)
        before = self.record_path().read_bytes()
        request["comparability"]["task_difficulty_band"] = "medium"
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "immutable conflicting admission"):
            self.admit(request)
        self.assertEqual(self.record_path().read_bytes(), before)

    def test_duplicate_case_or_assignment_evidence_is_refused(self) -> None:
        self.admit(self.request())
        duplicate = self.unique_case("chronik-natural-002")
        duplicate["assignment"] = dict(self.request()["assignment"])
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "assignment evidence is already bound"):
            self.admit(duplicate)
        self.assertFalse(self.record_path("chronik-natural-002").exists())

    def test_registration_drift_is_refused_for_existing_case(self) -> None:
        request = self.request()
        self.admit(request)
        before = self.record_path().read_bytes()
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        registration["decision_target"]["question"] = "Does a changed question invalidate the frozen admission binding?"
        self.registration.write_text(json.dumps(registration), encoding="utf-8")
        self.sync_active_registry()
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "immutable conflicting admission"):
            self.admit(request)
        self.assertEqual(self.record_path().read_bytes(), before)

    def test_registration_revision_does_not_poison_new_explicit_target(self) -> None:
        self.admit(self.unique_case("old-case", evidence_digit="4"))
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        registration["decision_target"]["question"] = "Should the revised decision question proceed?"
        self.registration.write_text(json.dumps(registration, indent=2) + "\n", encoding="utf-8")
        self.sync_active_registry()
        newer = self.unique_case("new-case", condition="live_preflight_plus_history", evidence_digit="5")
        self.admit(newer)
        current = json.loads(self.registration.read_text())
        record = ADMISSION.validate_existing_admission(self.registration, self.record_path("new-case"), current)
        self.assertEqual(record["frozen_request"]["case_id"], "new-case")

    def test_historical_automatic_registration_is_not_current_admission_mode(self) -> None:
        self.registration.write_bytes(ADMISSION.DEFAULT_REGISTRATION.read_bytes())
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "historical-only"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_planning_started_fixture_is_refused_before_creation(self) -> None:
        request = json.loads((FIXTURES / "invalid-backfill-request.json").read_text())
        request["assignment"] = self.request()["assignment"]
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "planning_started"):
            self.admit(request)
        self.assertFalse(self.admissions.exists())

    def test_pre_registration_case_is_refused_as_backfill(self) -> None:
        request = self.request()
        request["case_opened_at"] = "2026-07-12T23:59:00Z"
        request["eligibility_evidence"]["captured_at"] = "2026-07-12T23:59:30Z"
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "backfill refused"):
            self.admit(request)

    def test_post_expiry_admission_is_refused(self) -> None:
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "expired"):
            self.admit(self.request(), now=datetime(2026, 9, 1, tzinfo=timezone.utc))

    def test_two_explicit_cases_preserve_chosen_conditions(self) -> None:
        self.admit(self.unique_case("explicit-one", condition="live_preflight_only", evidence_digit="6"))
        self.admit(self.unique_case("explicit-two", condition="live_preflight_plus_history", evidence_digit="7"))
        one = json.loads(self.record_path("explicit-one").read_text())
        two = json.loads(self.record_path("explicit-two").read_text())
        self.assertEqual(one["assignment_evidence"]["condition"], "live_preflight_only")
        self.assertEqual(two["assignment_evidence"]["condition"], "live_preflight_plus_history")
        self.assertFalse(one["assignment_evidence"]["automatic"])
        self.assertFalse(two["assignment_evidence"]["automatic"])

    def test_current_v2_without_explicit_natural_case_capability_is_rejected(self) -> None:
        source = ROOT / "experiments/2026-08-24_outcome-bound-natural-pilot-sampling-unit-r3-v3/registration.v2.json"
        registration = json.loads(source.read_text(encoding="utf-8"))
        other = self.root / "experiments" / registration["experiment_id"]
        other.mkdir()
        registration_path = other / "registration.v2.json"
        registration_path.write_text(json.dumps(registration), encoding="utf-8")
        request = self.request(case_id="modern-natural-001", condition=registration["treatment_condition"]["id"])
        request["case_opened_at"] = "2026-08-25T10:00:00Z"
        request["eligibility_evidence"] = {"ref":"receipt:modern-natural-001","sha256":"9"*64,"captured_at":"2026-08-25T10:00:30Z"}
        request["triggered_by"] = "modern-natural-case-receipt-001"
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "does not explicitly authorize"):
            ADMISSION.admit(registration_path, self.write_request(request), other / "artifacts/admissions", now=datetime(2026,8,25,10,1,tzinfo=timezone.utc))
        self.assertFalse((other / "artifacts").exists())

    def test_inactive_registration_is_rejected_before_creation(self) -> None:
        registry_path = self.root / "experiments/active.v1.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["experiments"] = []
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "not uniquely present in the active registry"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_active_registry_registration_drift_is_rejected_before_creation(self) -> None:
        registry_path = self.root / "experiments/active.v1.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["experiments"][0]["primary_metric"] = "wrong_metric"
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "active registry contract invalid"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_active_registry_source_ref_must_be_canonical_decision(self) -> None:
        registry_path = self.root / "experiments/active.v1.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["experiments"][0]["source_ref"] = f"experiments/{self.experiment_id}/registration.v2.json"
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "source_ref must be exactly"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_active_registry_source_ref_traversal_is_rejected(self) -> None:
        registry_path = self.root / "experiments/active.v1.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["experiments"][0]["source_ref"] = f"experiments/{self.experiment_id}/results/../../outside.yml"
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "source_ref must be exactly"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_active_manifest_state_conflict_is_rejected(self) -> None:
        (self.experiment / "manifest.yml").write_text("experiment:\n  status: testing\n", encoding="utf-8")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "conflicts with manifest status"):
            self.admit(self.request())
        self.assertFalse(self.admissions.exists())

    def test_malformed_unrelated_sibling_does_not_block_valid_case(self) -> None:
        self.admit(self.unique_case("valid-one", evidence_digit="4"))
        malformed = self.admissions / "broken-neighbor"
        malformed.mkdir()
        (malformed / "admission.json").write_text("{not-json\n", encoding="utf-8")
        result = self.admit(
            self.unique_case("valid-two", condition="live_preflight_plus_history", evidence_digit="5")
        )
        self.assertEqual(result["status"], "admitted")
        self.assertTrue(self.record_path("valid-two").is_file())
        self.assertEqual((malformed / "admission.json").read_text(), "{not-json\n")

    def test_schema_valid_semantically_forged_sibling_has_no_dedupe_authority(self) -> None:
        self.admit(self.unique_case("valid-one", evidence_digit="4"))
        target = self.unique_case("target-case", evidence_digit="9")
        forged_request = self.unique_case("forged-neighbor", evidence_digit="8")
        forged_request["eligibility_evidence"] = dict(target["eligibility_evidence"])
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        forged = ADMISSION.build_record(
            forged_request,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(forged_request),
        )
        forged["request_sha256"] = "0" * 64
        forged_dir = self.admissions / "forged-neighbor"
        forged_dir.mkdir()
        (forged_dir / "admission.json").write_text(
            json.dumps(forged, indent=2) + "\n", encoding="utf-8"
        )
        result = self.admit(target)
        self.assertEqual(result["status"], "admitted")
        self.assertTrue(self.record_path("target-case").is_file())

    def test_hash_consistent_impossible_chronology_sibling_has_no_dedupe_authority(self) -> None:
        target = self.unique_case("chronology-target", evidence_digit="6")
        forged_request = self.unique_case("chronology-forged", evidence_digit="7")
        forged_request["eligibility_evidence"] = dict(target["eligibility_evidence"])
        forged_request["case_opened_at"] = "2026-08-11T06:55:00Z"
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        forged = ADMISSION.build_record(
            forged_request,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(forged_request),
        )
        forged_dir = self.admissions / "chronology-forged"
        forged_dir.mkdir(parents=True)
        (forged_dir / "admission.json").write_text(
            json.dumps(forged, indent=2) + "\n", encoding="utf-8"
        )
        result = self.admit(target)
        self.assertEqual(result["status"], "admitted")
        self.assertTrue(self.record_path("chronology-target").is_file())

    def test_hash_consistent_wrong_experiment_sibling_has_no_dedupe_authority(self) -> None:
        target = self.unique_case("experiment-target", evidence_digit="8")
        forged_request = self.unique_case("experiment-forged", evidence_digit="9")
        forged_request["eligibility_evidence"] = dict(target["eligibility_evidence"])
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        forged = ADMISSION.build_record(
            forged_request,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(forged_request),
        )
        forged["experiment_id"] = "2026-08-11_other-experiment"
        forged["admission_id"] = ADMISSION.sha256_json(
            {
                "schema_version": 1,
                "experiment_id": forged["experiment_id"],
                "registration_sha256": forged["registration_sha256"],
                "request_sha256": forged["request_sha256"],
                "assignment_evidence": forged["assignment_evidence"],
            }
        )
        forged["review_preparation"]["blinded_case_id"] = ADMISSION.sha256_json(
            {
                "schema_version": 1,
                "experiment_id": forged["experiment_id"],
                "case_id": forged_request["case_id"],
                "eligibility_evidence_sha256": forged_request["eligibility_evidence"]["sha256"],
                "comparability_sha256": forged["comparability_sha256"],
            }
        )
        forged_dir = self.admissions / "experiment-forged"
        forged_dir.mkdir(parents=True)
        (forged_dir / "admission.json").write_text(
            json.dumps(forged, indent=2) + "\n", encoding="utf-8"
        )
        result = self.admit(target)
        self.assertEqual(result["status"], "admitted")
        self.assertTrue(self.record_path("experiment-target").is_file())

    def test_hash_consistent_temporal_boundary_siblings_have_no_dedupe_authority(self) -> None:
        target = self.unique_case("temporal-target", evidence_digit="d")
        registration = json.loads(self.registration.read_text(encoding="utf-8"))

        before_start = self.unique_case("before-start-forged", evidence_digit="e")
        before_start["eligibility_evidence"] = dict(target["eligibility_evidence"])
        before_start["case_opened_at"] = "2026-08-10T23:59:00Z"
        forged_before_start = ADMISSION.build_record(
            before_start,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(before_start),
        )

        stale_review = self.unique_case("stale-review-forged", evidence_digit="f")
        stale_review["eligibility_evidence"] = dict(target["eligibility_evidence"])
        forged_stale_review = ADMISSION.build_record(
            stale_review,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(stale_review),
        )
        forged_stale_review["review_preparation"]["review_at"] = ADMISSION.format_utc(FIXED_NOW)

        for case_id, record in (
            ("before-start-forged", forged_before_start),
            ("stale-review-forged", forged_stale_review),
        ):
            forged_dir = self.admissions / case_id
            forged_dir.mkdir(parents=True)
            (forged_dir / "admission.json").write_text(
                json.dumps(record, indent=2) + "\n", encoding="utf-8"
            )

        result = self.admit(target)
        self.assertEqual(result["status"], "admitted")
        self.assertTrue(self.record_path("temporal-target").is_file())

    def test_semantically_forged_current_case_fails_closed(self) -> None:
        self.admit(self.unique_case("valid-one", evidence_digit="4"))
        request = self.unique_case("forged-current", evidence_digit="a")
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        forged = ADMISSION.build_record(
            request,
            registration,
            FIXED_NOW,
            ADMISSION._explicit_assignment_evidence(request),
        )
        forged["admission_id"] = "0" * 64
        forged_dir = self.admissions / "forged-current"
        forged_dir.mkdir()
        (forged_dir / "admission.json").write_text(
            json.dumps(forged, indent=2) + "\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(
            ADMISSION.AdmissionError, "current case already has a malformed or conflicting"
        ):
            self.admit(request)

    def test_valid_old_revision_receipt_keeps_global_dedupe_authority(self) -> None:
        old = self.unique_case("old-case", evidence_digit="b")
        self.admit(old)
        registration = json.loads(self.registration.read_text(encoding="utf-8"))
        registration["decision_target"]["question"] = "Should the revised decision question proceed?"
        self.registration.write_text(json.dumps(registration, indent=2) + "\n", encoding="utf-8")
        self.sync_active_registry()
        newer = self.unique_case(
            "new-case", condition="live_preflight_plus_history", evidence_digit="c"
        )
        newer["eligibility_evidence"] = dict(old["eligibility_evidence"])
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "eligibility evidence is already bound"):
            self.admit(newer)
        self.assertFalse(self.record_path("new-case").exists())

    def test_valid_receipt_keeps_dedupe_authority_with_unrelated_sibling_file(self) -> None:
        old = self.unique_case("old-case", evidence_digit="d")
        self.admit(old)
        sibling = self.admissions / "old-case" / "diagnostic.txt"
        sibling.write_text("non-authoritative diagnostic\n", encoding="utf-8")
        newer = self.unique_case(
            "new-case", condition="live_preflight_plus_history", evidence_digit="e"
        )
        newer["eligibility_evidence"] = dict(old["eligibility_evidence"])
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "eligibility evidence is already bound"):
            self.admit(newer)
        self.assertFalse(self.record_path("new-case").exists())
        self.assertEqual(sibling.read_text(encoding="utf-8"), "non-authoritative diagnostic\n")

    def test_target_outside_experiment_admissions_is_refused(self) -> None:
        outside = self.root / "outside-admissions"
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "must be the registered experiment"):
            ADMISSION.admit(self.registration, self.write_request(self.request()), outside, now=FIXED_NOW)
        self.assertFalse(outside.exists())

    def test_symlinked_artifacts_ancestor_is_refused_before_write(self) -> None:
        victim = self.root / "victim"
        victim.mkdir()
        (self.experiment / "artifacts").symlink_to(victim, target_is_directory=True)
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "must not traverse symlinks"):
            self.admit(self.request())
        self.assertEqual(list(victim.iterdir()), [])

    def test_symlinked_experiment_ancestor_is_refused_before_write(self) -> None:
        real = self.root / "real-experiment"
        real.mkdir()
        registration = json.loads(self.registration.read_text())
        (real / "registration.v2.json").write_text(json.dumps(registration))
        link = self.root / "linked-experiment"
        link.symlink_to(real, target_is_directory=True)
        request = self.write_request(self.request(), "symlink-request.json")
        with self.assertRaisesRegex(ADMISSION.AdmissionError, "must not traverse symlinks"):
            ADMISSION.admit(link / "registration.v2.json", request, link / "artifacts/admissions", now=FIXED_NOW)
        self.assertFalse((real / "artifacts").exists())

    def test_two_processes_preserve_one_create_only_record(self) -> None:
        request = self.request(case_id="concurrent-natural-001")
        request_path = self.write_request(request, "concurrent-request.json")
        context = multiprocessing.get_context("fork")
        output = context.Queue()
        processes = [context.Process(target=_process_admit, args=(self.registration, request_path, self.admissions, output)) for _ in range(2)]
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=20)
        results = [output.get(timeout=5) for _ in processes]
        self.assertEqual([process.exitcode for process in processes], [0, 0], results)
        self.assertEqual([status for status, _payload in results], ["ok", "ok"], results)
        payloads = [payload for _status, payload in results]
        self.assertEqual({payload["status"] for payload in payloads}, {"admitted", "already_admitted"})
        self.assertEqual(len(list(self.admissions.rglob("admission.json"))), 1)


if __name__ == "__main__":
    unittest.main()
