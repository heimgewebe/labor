#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import multiprocessing
import tempfile
import unittest
from unittest import mock
from pathlib import Path

SCRIPT = Path(__file__).with_name("capture_effect_observation.py")
SPEC = importlib.util.spec_from_file_location("capture_effect_observation", SCRIPT)
assert SPEC and SPEC.loader
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)
ADMIT_SCRIPT = Path(__file__).with_name("admit_natural_case.py")
ADMIT_SPEC = importlib.util.spec_from_file_location("admit_natural_case_for_capture", ADMIT_SCRIPT)
assert ADMIT_SPEC and ADMIT_SPEC.loader
ADMISSION = importlib.util.module_from_spec(ADMIT_SPEC)
ADMIT_SPEC.loader.exec_module(ADMISSION)


def _process_capture(registration: Path, observations: Path, row: dict, output: multiprocessing.Queue) -> None:
    try:
        output.put(("ok", CAPTURE.capture(registration, observations, row)))
    except Exception as exc:
        output.put(("error", f"{type(exc).__name__}: {exc}"))


class CaptureEffectObservationTests(unittest.TestCase):
    def setUp(self) -> None:
        grandfathered = mock.patch.object(
            CAPTURE.REGISTRATION_GATE,
            "is_pre_t005_registration_artifact",
            return_value=True,
        )
        grandfathered.start()
        self.addCleanup(grandfathered.stop)

    def registration(self) -> dict:
        return {
            "schema_version": "experiment.registration.v2",
            "experiment_id": "2026-07-12_operator-intervention-effect-evaluator",
            "registered_at": "2026-07-31T00:00:00Z",
            "consumer": {
                "organ": "bureau",
                "use": "Use reviewed results to decide whether the intervention remains active.",
                "relationship": "external",
                "commitment": {
                    "status": "confirmed",
                    "evidence_ref": "bureau:capture-example-consumer",
                    "confirmed_at": "2026-07-31T00:00:00Z",
                    "valid_until": "2099-10-01T00:00:00Z",
                },
            },
            "decision_target": {
                "question": "Should the intervention remain active after the pilot?",
                "owner": "bureau",
                "decision_ref": "bureau:capture-example-decision",
            },
            "intervention": {
                "name": "effect_capture",
                "description": "Capture evidence-bound observations before deterministic review.",
            },
            "control_condition": {
                "id": "manual_review",
                "description": "Review the evidence manually without the effect report.",
            },
            "treatment_condition": {
                "id": "evaluator_assisted_review",
                "description": "Review the same evidence with the deterministic effect report.",
            },
            "measurement": {
                "primary_metric": "reviewed_decision_value_score",
                "direction": "higher_is_better",
                "unit": "score",
                "minimum_material_effect": 1,
                "cost_metric": {
                    "id": "review_effort_seconds",
                    "unit": "seconds",
                    "method": "Measure elapsed review effort for each decision.",
                },
                "method": "Compare evidence-bound paired review observations.",
                "success": "A material favorable effect without overclaiming.",
                "falsification": "No material effect, harm, or misleading evidence use.",
                "outcome_criteria": {
                    "success_threshold": 2,
                    "harm_or_falsification_threshold": 0,
                },
            },
            "comparison": {
                "mode": "paired",
                "unit": "same frozen evidence and decision question",
                "minimum_control": 3,
                "minimum_treatment": 3,
                "comparability_constraints": [
                    "same frozen evidence",
                    "same decision question",
                ],
                "confounders": ["reviewer expertise"],
            },
            "evidence_sources": {
                "allowed": ["typed execution receipt"],
                "independent_observation_required": True,
            },
            "review_at": "2099-09-15T00:00:00Z",
            "expires_at": "2099-10-01T00:00:00Z",
            "closure": {
                "allowed_outcomes": ["promote", "pilot", "defer", "reject", "archive"],
                "archive_path": "experiments/_archive/2026-07-12_operator-intervention-effect-evaluator",
                "outcome_by_result": {
                    "success": "promote",
                    "harm_or_falsification": "reject",
                    "inconclusive": "defer",
                    "expired": "archive",
                },
            },
            "surface_budget": {
                "durable_additions": [],
                "durable_offsets": [],
                "reviewed_exception": None,
            },
            "boundary": {
                "experiment_only": True,
                "no_auto_policy": True,
                "no_auto_routing": True,
                "no_queue_authority": True,
                "no_runtime_authority": True,
                "no_merge_authority": True,
            },
        }

    def setup_experiment(self, root: Path) -> tuple[Path, Path]:
        experiment = root / "experiments/2026-07-12_operator-intervention-effect-evaluator"
        results = experiment / "results"
        results.mkdir(parents=True)
        registration = experiment / "registration.v2.json"
        registration.write_text(json.dumps(self.registration()), encoding="utf-8")
        return registration, results / "observations.v2.json"

    def observation(self, identifier: str = "manual-1", *, digest_seed: str = "evidence-1") -> dict:
        return {
            "observation_id": identifier,
            "condition": "manual_review",
            "value": 2.0,
            "effort_seconds": 60.0,
            "scoring_blinded": True,
            "comparison_key": "pilot-1",
            "pair_id": "pilot-1",
            "evidence_ref": f"receipt:{identifier}",
            "evidence_sha256": hashlib.sha256(digest_seed.encode()).hexdigest(),
            "decision_maker_ref": f"receipt:decider-{identifier}",
            "observer_ref": f"receipt:observer-{identifier}",
            "independent": True,
            "captured_at": "2026-08-01T00:00:00Z",
        }

    def test_capture_creates_registration_bound_document(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            result = CAPTURE.capture(registration, observations, self.observation())
            document = json.loads(observations.read_text(encoding="utf-8"))
            expected_registration = CAPTURE.sha256_json(self.registration())
            self.assertEqual(document["registration_sha256"], expected_registration)
            self.assertEqual(document["observations"][0]["observation_id"], "manual-1")
            self.assertEqual(result["observation_count"], 1)

    def test_registration_drift_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            CAPTURE.capture(registration, observations, self.observation())
            before = observations.read_bytes()
            changed = self.registration()
            changed["decision_target"]["question"] = "Should the changed intervention remain active?"
            registration.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaisesRegex(CAPTURE.CaptureError, "registration digest mismatch"):
                CAPTURE.capture(
                    registration,
                    observations,
                    self.observation("manual-2", digest_seed="evidence-2"),
                )
            self.assertEqual(observations.read_bytes(), before)

    def test_duplicate_evidence_digest_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            CAPTURE.capture(registration, observations, self.observation())
            before = observations.read_bytes()
            with self.assertRaisesRegex(CAPTURE.CaptureError, "duplicate evidence_sha256"):
                CAPTURE.capture(
                    registration,
                    observations,
                    self.observation("manual-2", digest_seed="evidence-1"),
                )
            self.assertEqual(observations.read_bytes(), before)

    def test_duplicate_condition_within_pair_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            CAPTURE.capture(registration, observations, self.observation("manual-1"))
            before = observations.read_bytes()
            duplicate = self.observation("manual-2", digest_seed="evidence-2")
            duplicate["pair_id"] = "pilot-1"
            with self.assertRaisesRegex(CAPTURE.CaptureError, "duplicate condition within pair"):
                CAPTURE.capture(registration, observations, duplicate)
            self.assertEqual(observations.read_bytes(), before)

    def test_expired_registration_still_blocks_new_capture(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            expired = self.registration()
            expired["registered_at"] = "2026-07-13T00:00:00Z"
            expired["consumer"]["commitment"]["confirmed_at"] = "2026-07-13T00:00:00Z"
            expired["consumer"]["commitment"]["valid_until"] = "2026-08-02T00:00:00Z"
            expired["review_at"] = "2026-07-20T00:00:00Z"
            expired["expires_at"] = "2026-08-02T00:00:00Z"
            registration.write_text(json.dumps(expired), encoding="utf-8")
            row = self.observation()
            row["captured_at"] = "2026-08-01T00:00:00Z"
            with self.assertRaisesRegex(CAPTURE.CaptureError, "registration already expired"):
                CAPTURE.capture(registration, observations, row)
            self.assertFalse(observations.exists())

    def test_expired_observation_is_rejected_before_file_creation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            row = self.observation()
            row["captured_at"] = "2099-10-01T00:00:01Z"
            with self.assertRaisesRegex(CAPTURE.CaptureError, "after experiment expiry"):
                CAPTURE.capture(registration, observations, row)
            self.assertFalse(observations.exists())

    def test_target_outside_results_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            registration, _observations = self.setup_experiment(root)
            outside = root / "outside.json"
            with self.assertRaisesRegex(CAPTURE.CaptureError, "inside the registered experiment results"):
                CAPTURE.capture(registration, outside, self.observation())
            self.assertFalse(outside.exists())

    def test_symlink_target_is_rejected_without_touching_victim(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            registration, observations = self.setup_experiment(root)
            victim = root / "victim.json"
            victim.write_text("victim\n", encoding="utf-8")
            observations.symlink_to(victim)
            with self.assertRaisesRegex(CAPTURE.CaptureError, "must not be a symlink"):
                CAPTURE.capture(registration, observations, self.observation())
            self.assertEqual(victim.read_text(encoding="utf-8"), "victim\n")

    def test_registered_scorecard_computes_value_from_components(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            registration, observations = self.setup_experiment(root)
            data = self.registration()
            data["measurement"]["scorecard"] = {
                "schema_version": "additive-binary-scorecard.v1",
                "components": [
                    {"id": "aligned", "weight": 2, "criterion": "Decision aligns with adjudication."},
                    {"id": "calibrated", "weight": 1, "criterion": "Decision preserves uncertainty."},
                ],
            }
            registration.write_text(json.dumps(data), encoding="utf-8")
            evidence = root / "scorecard.json"
            evidence.write_text("{}\n", encoding="utf-8")
            parser_args = type("Args", (), {
                "evidence_sha256": None,
                "evidence_file": evidence,
                "independent": True,
                "value": None,
                "score_component": ["aligned=1", "calibrated=0"],
                "effort_seconds": "75",
                "scoring_blinded": True,
                "observation_id": "manual-score",
                "condition": "manual_review",
                "comparison_key": "pilot-score",
                "evidence_ref": "receipt:manual-score",
                "decision_maker_ref": "receipt:decider-score",
                "observer_ref": "receipt:observer-score",
                "captured_at": "2026-08-01T00:00:00Z",
                "pair_id": "pilot-score",
            })()
            row = CAPTURE.build_observation(parser_args, data)
            self.assertEqual(row["value"], 2.0)
            self.assertEqual(row["score_components"], {"aligned": 1, "calibrated": 0})
            CAPTURE.capture(registration, observations, row)

    def test_self_scored_observation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            row = self.observation()
            row["observer_ref"] = row["decision_maker_ref"]
            with self.assertRaisesRegex(CAPTURE.CaptureError, "scorer must differ"):
                CAPTURE.capture(registration, observations, row)
            self.assertFalse(observations.exists())

    def test_evidence_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "evidence.json"
            target.write_text("{}\n", encoding="utf-8")
            link = root / "evidence-link.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(CAPTURE.CaptureError, "must not be a symlink"):
                CAPTURE.sha256_file(link)

    def test_negative_effort_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            registration, observations = self.setup_experiment(Path(raw))
            row = self.observation()
            row["effort_seconds"] = -1
            with self.assertRaisesRegex(CAPTURE.CaptureError, "effort_seconds"):
                CAPTURE.capture(registration, observations, row)
            self.assertFalse(observations.exists())

    def test_concurrent_writers_are_all_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            registration, observations = self.setup_experiment(root)
            rows = []
            for index in range(4):
                row = self.observation(f"obs-{index}", digest_seed=f"evidence-{index}")
                row["comparison_key"] = f"pilot-concurrent-{index}"
                row["pair_id"] = f"pilot-{index}"
                rows.append(row)
            context = multiprocessing.get_context("fork")
            output = context.Queue()
            processes = [
                context.Process(target=_process_capture, args=(registration, observations, row, output))
                for row in rows
            ]
            for process in processes:
                process.start()
            for process in processes:
                process.join(timeout=20)
            results = [output.get(timeout=5) for _ in processes]
            self.assertEqual([process.exitcode for process in processes], [0, 0, 0, 0], results)
            self.assertEqual([status for status, _payload in results], ["ok", "ok", "ok", "ok"], results)
            document = json.loads(observations.read_text(encoding="utf-8"))
            self.assertEqual(
                [row["observation_id"] for row in document["observations"]],
                ["obs-0", "obs-1", "obs-2", "obs-3"],
            )



class ChronikAdmissionBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.registration, self.admission, self.observations, self._row = self.explicit_case()
        record = json.loads(self.admission.read_text())
        self.condition = record["assignment_evidence"]["condition"]
        self.blinded = record["review_preparation"]["blinded_case_id"]
        self.comparison_key = record["frozen_request"]["comparability"]["comparison_key"]

    def row(self) -> dict:
        return json.loads(json.dumps(self._row))

    def explicit_case(self) -> tuple[Path, Path, Path, dict]:
        experiment_id = "2026-09-12_zero-to-decision-explicit"
        exp = self.root / "experiments" / experiment_id
        (exp / "results").mkdir(parents=True)
        registration_path = exp / "registration.v2.json"
        registration = CaptureEffectObservationTests().registration()
        registration["experiment_id"] = experiment_id
        registration["natural_case_admission"] = True
        registration["closure"]["archive_path"] = f"experiments/_archive/{experiment_id}"
        registration_path.write_text(json.dumps(registration, indent=2) + "\n")
        decision = exp / "results/decision.yml"
        decision.write_text("verdict: not_executed\n", encoding="utf-8")
        active = {
            "schema_version": "active-experiments.v1",
            "max_active": 5,
            "experiments": [{
                "experiment_id": experiment_id,
                "path": f"experiments/{experiment_id}",
                "state": "designed",
                "consumer": registration["consumer"]["organ"],
                "decision_target": registration["decision_target"]["question"],
                "primary_metric": registration["measurement"]["primary_metric"],
                "review_at": registration["review_at"],
                "expires_at": registration["expires_at"],
                "source_ref": f"experiments/{experiment_id}/results/decision.yml",
            }],
        }
        (self.root / "experiments/active.v1.json").write_text(json.dumps(active, indent=2) + "\n", encoding="utf-8")
        request = json.loads((CAPTURE.ROOT / "tests/fixtures/natural_case_admission/valid-control-request.json").read_text())
        request["case_id"] = "explicit-case-1"
        request["case_opened_at"] = "2026-09-12T16:00:00Z"
        request["eligibility_evidence"]["captured_at"] = "2026-09-12T16:00:01Z"
        request["assignment"] = {
            "condition": registration["control_condition"]["id"],
            "assigned_by": "operator:prospective",
            "evidence_ref": "receipt:explicit-assignment-case-1",
            "evidence_sha256": "d" * 64,
            "recorded_before_planning": True,
        }
        request_path = self.root / "explicit-request.json"
        request_path.write_text(json.dumps(request, indent=2) + "\n")
        admitted = ADMISSION.admit(
            registration_path, request_path, exp / "artifacts/admissions",
            now=ADMISSION.utc_timestamp("2026-09-12T16:00:02Z", "test-now"),
        )
        admission_path = Path(admitted["path"])
        record = json.loads(admission_path.read_text())
        row = {
            "observation_id": record["review_preparation"]["blinded_case_id"],
            "condition": record["assignment_evidence"]["condition"],
            "value": 2.0,
            "effort_seconds": 30.0,
            "scoring_blinded": True,
            "comparison_key": record["frozen_request"]["comparability"]["comparison_key"],
            "evidence_ref": "receipt:explicit-case-1-outcome",
            "evidence_sha256": "e" * 64,
            "decision_maker_ref": "receipt:decision-explicit-case-1",
            "observer_ref": "receipt:reviewer-explicit-case-1",
            "independent": True,
            "captured_at": "2026-09-12T16:05:00Z",
        }
        return registration_path, admission_path, exp / "results/observations.v2.json", row

    def test_forged_explicit_condition_is_rejected_even_when_observation_matches_forgery(self) -> None:
        record = json.loads(self.admission.read_text())
        forged = (
            "live_preflight_plus_history"
            if record["assignment_evidence"]["condition"] == "live_preflight_only"
            else "live_preflight_only"
        )
        record["assignment_evidence"]["condition"] = forged
        self.admission.chmod(0o644)
        self.admission.write_text(json.dumps(record, indent=2) + "\n")
        row = self.row()
        row["condition"] = forged
        with self.assertRaisesRegex(CAPTURE.CaptureError, "semantic commitments"):
            CAPTURE.capture(self.registration, self.observations, row, admission_path=self.admission)

    def test_semantically_forged_admission_is_rejected(self) -> None:
        record = json.loads(self.admission.read_text())
        record["request_sha256"] = "0" * 64
        self.admission.chmod(0o644)
        self.admission.write_text(json.dumps(record, indent=2) + "\n")
        with self.assertRaisesRegex(CAPTURE.CaptureError, "request digest mismatch"):
            CAPTURE.capture(self.registration, self.observations, self.row(), admission_path=self.admission)

    def test_valid_observation_is_bound_to_admission(self) -> None:
        CAPTURE.capture(self.registration, self.observations, self.row(), admission_path=self.admission)
        stored = json.loads(self.observations.read_text())["observations"][0]
        self.assertEqual(stored["admission_binding"]["case_id"], "explicit-case-1")
        self.assertEqual(stored["admission_binding"]["blinded_case_id"], self.blinded)
        self.assertEqual(stored["admission_binding"]["admission_sha256"], CAPTURE.sha256_file(self.admission))

    def test_current_observation_before_registration_is_rejected(self) -> None:
        row = self.row()
        row["captured_at"] = "2026-07-30T23:59:59Z"
        with self.assertRaisesRegex(CAPTURE.CaptureError, "before experiment registration"):
            CAPTURE.capture(self.registration, self.observations, row, admission_path=self.admission)

    def test_current_t005_semantic_gate_runs_before_capture(self) -> None:
        invalid = json.loads(self.registration.read_text())
        del invalid["registered_at"]
        self.registration.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaisesRegex(CAPTURE.CaptureError, "registered_at"):
            CAPTURE.capture(self.registration, self.observations, self.row(), admission_path=self.admission)

    def test_replayed_pre_t005_id_outside_canonical_archive_still_requires_admission(self) -> None:
        experiment_id = "2026-07-12_operator-intervention-effect-evaluator"
        exp = self.root / "replayed" / "experiments" / experiment_id
        (exp / "results").mkdir(parents=True)
        registration = CaptureEffectObservationTests().registration()
        registration["experiment_id"] = experiment_id
        registration["closure"]["archive_path"] = f"experiments/_archive/{experiment_id}"
        registration_path = exp / "registration.v2.json"
        registration_path.write_text(json.dumps(registration, indent=2) + "\n")
        with self.assertRaisesRegex(CAPTURE.CaptureError, "requires --admission"):
            CAPTURE.capture(registration_path, exp / "results/observations.v2.json", self.row())

    def test_current_observation_without_admission_is_rejected(self) -> None:
        with self.assertRaisesRegex(CAPTURE.CaptureError, "requires --admission"):
            CAPTURE.capture(self.registration, self.observations, self.row())

    def test_historical_automatic_registration_is_rejected_by_current_capture(self) -> None:
        source = CAPTURE.ROOT / "experiments/_archive/2026-07-13_chronik-history-brief-effect/registration.v2.json"
        original = CAPTURE.REGISTRATION_GATE.validate_registration
        frozen_now = ADMISSION.utc_timestamp("2026-08-11T06:50:00Z", "test-now")
        with mock.patch.object(
            CAPTURE.REGISTRATION_GATE,
            "validate_registration",
            side_effect=lambda path, **kwargs: original(path, now=frozen_now, **kwargs),
        ):
            with self.assertRaisesRegex(CAPTURE.CaptureError, "historical-only"):
                CAPTURE.capture(source, self.root / "unused-observations.json", self.row())

    def test_symlinked_artifacts_ancestor_is_rejected_by_capture(self) -> None:
        artifacts = self.registration.parent / "artifacts"
        external = self.root / "external-artifacts"
        artifacts.rename(external)
        artifacts.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(CAPTURE.CaptureError, "traverse symlinks"):
            CAPTURE.capture(self.registration, self.observations, self.row(), admission_path=self.admission)

    def test_condition_drift_is_rejected(self) -> None:
        row = self.row(); row["condition"] = "live_preflight_plus_history" if self.condition == "live_preflight_only" else "live_preflight_only"
        with self.assertRaisesRegex(CAPTURE.CaptureError, "condition does not match"):
            CAPTURE.capture(self.registration, self.observations, row, admission_path=self.admission)

    def test_comparison_key_drift_is_rejected(self) -> None:
        row = self.row(); row["comparison_key"] = "other-key"
        with self.assertRaisesRegex(CAPTURE.CaptureError, "comparison_key does not match"):
            CAPTURE.capture(self.registration, self.observations, row, admission_path=self.admission)

    def test_unblinded_identifier_is_rejected(self) -> None:
        row = self.row(); row["observation_id"] = "not-blinded"
        with self.assertRaisesRegex(CAPTURE.CaptureError, "blinded_case_id"):
            CAPTURE.capture(self.registration, self.observations, row, admission_path=self.admission)



if __name__ == "__main__":
    unittest.main()
