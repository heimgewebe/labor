#!/usr/bin/env python3
"""Publish one registration-bound natural case before planning.

The current zero-to-decision path accepts only explicit prospective condition
assignments backed by external evidence. Historical automatic-assignment
registrations remain valid archive facts but are not an active admission mode.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, ValidationError


ROOT = Path(__file__).resolve().parents[2]
ADMISSION_SCHEMA = ROOT / "schemas/natural-case-admission.v1.schema.json"
ACTIVE_REGISTRY_SCHEMA = ROOT / "schemas/active-experiments.v1.schema.json"
REGISTRATION_GATE_PATH = ROOT / "scripts/docmeta/validate_experiment_registration.py"
# Historical fixture paths retained for regression tests only. The CLI has no
# experiment default and derives the admissions directory from --registration.
DEFAULT_EXPERIMENT = ROOT / "experiments/_archive/2026-07-13_chronik-history-brief-effect"
DEFAULT_REGISTRATION = DEFAULT_EXPERIMENT / "registration.v2.json"
DEFAULT_ADMISSIONS = DEFAULT_EXPERIMENT / "artifacts/admissions"
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
ADMISSION_BOUNDARY_KEYS = (
    "experiment_only",
    "no_auto_policy",
    "no_auto_routing",
    "no_queue_authority",
    "no_runtime_authority",
)
MANUAL_NON_CLAIMS = [
    "automatic_assignment",
    "assignment_fairness",
    "external_eligibility_truth",
    "case_execution",
    "independent_review_completion",
    "condition_effect",
    "routing_queue_or_runtime_authority",
]

class AdmissionError(RuntimeError):
    pass


def _load_registration_gate() -> Any:
    spec = importlib.util.spec_from_file_location("labor_registration_gate_admission", REGISTRATION_GATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load registration gate from {REGISTRATION_GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REGISTRATION_GATE = _load_registration_gate()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode(
        "utf-8"
    )


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def load_object(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise AdmissionError(f"{label} must be a regular non-symlink file")
    if path.stat().st_size > 1_000_000:
        raise AdmissionError(f"{label} exceeds 1 MiB")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdmissionError(f"{label} must contain UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise AdmissionError(f"{label} must contain an object")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    return load_object(path, f"schema {path.name}")


def validator(schema: dict[str, Any]) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate(value: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    try:
        validator(schema).validate(value)
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        suffix = f" at {location}" if location else ""
        raise AdmissionError(f"{label} is invalid{suffix}: {exc.message}") from exc


def utc_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise AdmissionError(f"{label} must be an RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise AdmissionError(f"{label} must include a timezone")
    normalized = parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if value != normalized:
        raise AdmissionError(f"{label} must be canonical UTC-Z")
    return parsed.astimezone(timezone.utc)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def experiment_start(experiment_id: str) -> datetime:
    try:
        return datetime.fromisoformat(experiment_id[:10]).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise AdmissionError("experiment_id has no valid date prefix") from exc


def validate_registration(
    registration: dict[str, Any],
    registration_path: Path,
    *,
    now: datetime,
) -> None:
    if registration.get("assignment") is not None:
        raise AdmissionError("registered automatic assignment is historical-only; current admissions require explicit prospective assignment evidence")
    try:
        validated = REGISTRATION_GATE.validate_registration(registration_path, now=now, require_current=True)
    except Exception as exc:
        raise AdmissionError(f"registration contract invalid: {exc}") from exc
    if validated != registration:
        raise AdmissionError("registration payload changed while validating")
    if registration.get("schema_version") != "experiment.registration.v2":
        raise AdmissionError("natural-case admission requires registration.v2")
    if registration.get("natural_case_admission") is not True:
        raise AdmissionError("registration does not explicitly authorize natural-case admission")
    if any(registration["boundary"].get(key) is not True for key in ADMISSION_BOUNDARY_KEYS):
        raise AdmissionError("registration authority boundary is not closed")


def validate_active_registry_binding(registration_path: Path, registration: dict[str, Any], *, now: datetime) -> None:
    reject_symlink_chain(registration_path, "registration path")
    registration_absolute = registration_path.absolute()
    experiment_root = registration_absolute.parent
    experiments_root = experiment_root.parent
    experiment_id = registration["experiment_id"]
    if registration_absolute.name != "registration.v2.json" or experiments_root.name != "experiments" or experiment_root.name != experiment_id:
        raise AdmissionError("natural-case admission requires the canonical active experiment registration path")
    registry_path = experiments_root / "active.v1.json"
    reject_symlink_chain(registry_path, "active registry path")
    registry = load_object(registry_path, "active experiment registry")
    validate(registry, load_schema(ACTIVE_REGISTRY_SCHEMA), "active experiment registry")
    matches = [item for item in registry["experiments"] if item["experiment_id"] == experiment_id]
    if len(matches) != 1:
        raise AdmissionError("experiment is not uniquely present in the active registry")
    item = matches[0]
    expected = {"path": f"experiments/{experiment_id}", "consumer": registration["consumer"]["organ"], "decision_target": registration["decision_target"]["question"], "primary_metric": registration["measurement"]["primary_metric"], "review_at": registration["review_at"], "expires_at": registration["expires_at"]}
    conflicts = [key for key,value in expected.items() if item.get(key) != value]
    if conflicts:
        raise AdmissionError("active registry binding conflicts with registration: " + ", ".join(sorted(conflicts)))
    if utc_timestamp(item["expires_at"], "active registry expires_at") <= now:
        raise AdmissionError("active registry binding is expired")
    source_path = (experiments_root.parent / item["source_ref"]).absolute()
    reject_symlink_chain(source_path, "active registry source_ref")
    try:
        source_path.relative_to(experiment_root)
    except ValueError as exc:
        raise AdmissionError("active registry source_ref escapes the registered experiment") from exc
    if not source_path.is_file():
        raise AdmissionError("active registry source_ref is missing")


def request_schema(admission_schema: dict[str, Any]) -> dict[str, Any]:
    schema = admission_schema.get("$defs", {}).get("request")
    if not isinstance(schema, dict):
        raise AdmissionError("admission schema is missing $defs.request")
    return {
        "$schema": admission_schema["$schema"],
        **schema,
        "$defs": admission_schema["$defs"],
    }


def validate_request_semantics(
    request: dict[str, Any], registration: dict[str, Any], admitted: datetime
) -> None:
    case_id = request["case_id"]
    if CASE_ID_RE.fullmatch(case_id) is None:
        raise AdmissionError("case_id is not path-safe")

    eligibility = request["eligibility"]
    retrospective_signals = {
        "planning_started": eligibility["planning_started"],
        "execution_started": eligibility["execution_started"],
        "outcome_known": eligibility["outcome_known"],
        "prior_observation": eligibility["prior_observation"],
    }
    if any(retrospective_signals.values()):
        names = sorted(name for name, enabled in retrospective_signals.items() if enabled)
        raise AdmissionError("retrospective or backfill admission refused: " + ", ".join(names))
    if eligibility["natural_case"] is not True or eligibility["within_registered_scope"] is not True:
        raise AdmissionError("case is not attested as a natural in-scope case")
    if request["assignment"]["recorded_before_planning"] is not True:
        raise AdmissionError("assignment must be recorded before planning")

    opened = utc_timestamp(request["case_opened_at"], "case_opened_at")
    evidence_captured = utc_timestamp(
        request["eligibility_evidence"]["captured_at"], "eligibility_evidence.captured_at"
    )
    start = experiment_start(registration["experiment_id"])
    expiry = utc_timestamp(registration["expires_at"], "registration.expires_at")
    if admitted < start:
        raise AdmissionError("admission predates the registered experiment")
    if admitted >= expiry:
        raise AdmissionError("experiment is expired; admission refused")
    if opened < start:
        raise AdmissionError("case predates the registered experiment; backfill refused")
    if opened > admitted:
        raise AdmissionError("case_opened_at is after admission")
    if evidence_captured < opened or evidence_captured > admitted:
        raise AdmissionError("eligibility evidence must be captured between case opening and admission")

    if registration.get("assignment") is not None:
        raise AdmissionError(
            "registered automatic assignment is historical-only; current admissions require "
            "explicit prospective assignment evidence"
        )
    assignment = request["assignment"]
    conditions = {
        registration["control_condition"]["id"],
        registration["treatment_condition"]["id"],
    }
    if assignment.get("condition") not in conditions:
        raise AdmissionError("assignment condition is not registered")


def build_record(request: dict[str, Any], registration: dict[str, Any], admitted: datetime, assignment_evidence: dict[str, Any]) -> dict[str, Any]:
    registration_digest = sha256_json(registration)
    request_digest = sha256_json(request)
    comparability_digest = sha256_json(request["comparability"])
    blinded_case_id = sha256_json(
        {
            "schema_version": 1,
            "experiment_id": registration["experiment_id"],
            "case_id": request["case_id"],
            "eligibility_evidence_sha256": request["eligibility_evidence"]["sha256"],
            "comparability_sha256": comparability_digest,
        }
    )
    admission_id = sha256_json(
        {
            "schema_version": 1,
            "experiment_id": registration["experiment_id"],
            "registration_sha256": registration_digest,
            "request_sha256": request_digest,
            "assignment_evidence": assignment_evidence,
        }
    )
    return {
        "schema_version": "natural-case-admission.v1",
        "experiment_id": registration["experiment_id"],
        "registration_sha256": registration_digest,
        "admission_id": admission_id,
        "admitted_at": format_utc(admitted),
        "request_sha256": request_digest,
        "frozen_request": request,
        "comparability_sha256": comparability_digest,
        "assignment_evidence": assignment_evidence,
        "review_preparation": {
            "status": "pending_independent_review",
            "blinded_case_id": blinded_case_id,
            "blinding_required": True,
            "condition_disclosure": "after_score_seal",
            "independent_observation_required": registration["evidence_sources"][
                "independent_observation_required"
            ],
            "measurement_sha256": sha256_json(registration["measurement"]),
            "allowed_evidence_sources": registration["evidence_sources"]["allowed"],
            "minimum_control": registration["comparison"]["minimum_control"],
            "minimum_treatment": registration["comparison"]["minimum_treatment"],
            "review_at": registration["review_at"],
        },
        "boundary": {key: registration["boundary"][key] for key in ADMISSION_BOUNDARY_KEYS},
        "traceability": {
            "triggered_by": request["triggered_by"],
            "policy": "registration.v2.json + method.md",
            "action": "prospective_natural_case_admission",
            "outcome": "explicit_condition_assignment_sealed",
        },
        "non_claims": list(MANUAL_NON_CLAIMS),
    }


def _secure_lock_root() -> Path:
    runtime = os.environ.get("XDG_RUNTIME_DIR")
    candidates = []
    if runtime:
        candidates.append(Path(runtime) / f"vibe-lab-admission-locks-{os.getuid()}")
    candidates.append(Path(tempfile.gettempdir()) / f"vibe-lab-admission-locks-{os.getuid()}")
    failures: list[str] = []
    for candidate in candidates:
        try:
            candidate.mkdir(mode=0o700, parents=True, exist_ok=True)
            info = candidate.lstat()
        except OSError as exc:
            failures.append(f"{candidate}: {exc}")
            continue
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            failures.append(f"{candidate}: not a real directory")
            continue
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            failures.append(f"{candidate}: unsafe ownership or permissions")
            continue
        return candidate
    raise AdmissionError("cannot prepare a private admission lock directory: " + "; ".join(failures))


def _lock_fd(admissions_root: Path) -> int:
    lock_name = hashlib.sha256(os.fsencode(str(admissions_root.resolve(strict=False)))).hexdigest()
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(_secure_lock_root() / f"{lock_name}.lock", flags, 0o600)
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid():
        os.close(fd)
        raise AdmissionError("admission lock is not a safe regular file")
    return fd


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def publish_create_only(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=False, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    published = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(canonical_json_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o444)
        try:
            os.link(temporary, path, follow_symlinks=False)
        except FileExistsError as exc:
            raise AdmissionError("admission already exists") from exc
        published = True
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)
        if published:
            _fsync_directory(path.parent)


def reject_symlink_chain(path: Path, label: str) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(info.st_mode):
            raise AdmissionError(f"{label} must not traverse symlinks")


def safe_admissions_root(registration_path: Path, admissions_dir: Path) -> Path:
    reject_symlink_chain(registration_path, "registration path")
    experiment_root = registration_path.absolute().parent
    reject_symlink_chain(experiment_root, "experiment path")
    artifacts = experiment_root / "artifacts"
    expected = artifacts / "admissions"
    if admissions_dir.absolute() != expected:
        raise AdmissionError("admissions directory must be the registered experiment artifacts/admissions path")
    reject_symlink_chain(artifacts, "experiment artifacts path")
    artifacts.mkdir(parents=False, exist_ok=True)
    reject_symlink_chain(artifacts, "experiment artifacts path")
    admissions_dir.mkdir(mode=0o700, parents=False, exist_ok=True)
    reject_symlink_chain(admissions_dir, "admissions path")
    if not admissions_dir.is_dir():
        raise AdmissionError("admissions directory is unsafe")
    return admissions_dir


def existing_records(root: Path, schema: dict[str, Any]) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for case_dir in sorted(root.iterdir()):
        if case_dir.is_symlink() or not case_dir.is_dir():
            raise AdmissionError("unexpected non-directory entry in admissions root")
        entries = list(case_dir.iterdir())
        if len(entries) != 1 or entries[0].name != "admission.json":
            raise AdmissionError("admission case directory must contain only admission.json")
        path = entries[0]
        value = load_object(path, "existing admission")
        validate(value, schema, "existing admission")
        if value["frozen_request"]["case_id"] != case_dir.name:
            raise AdmissionError("existing admission case_id does not match its directory")
        records.append((path, value))
    return records


def validate_existing_admission(
    registration_path: Path,
    admission_path: Path,
    registration: dict[str, Any],
) -> dict[str, Any]:
    """Recompute one explicit admission's semantic commitments from file truth."""
    if registration.get("assignment") is not None:
        raise AdmissionError(
            "registered automatic assignment is historical-only; current admission consumption "
            "requires explicit prospective assignment evidence"
        )
    if registration.get("natural_case_admission") is not True:
        raise AdmissionError("registration does not explicitly authorize natural-case admission")
    reject_symlink_chain(registration_path, "registration path")
    experiment_root = registration_path.absolute().parent
    reject_symlink_chain(experiment_root, "experiment path")
    root = experiment_root / "artifacts" / "admissions"
    reject_symlink_chain(root, "admissions path")
    if not root.is_dir():
        raise AdmissionError("admissions root must be a real directory")
    admission_absolute = admission_path.absolute()
    reject_symlink_chain(admission_absolute, "admission path")
    try:
        relative = admission_absolute.relative_to(root)
    except ValueError as exc:
        raise AdmissionError("admission must be inside the registered experiment admissions directory") from exc
    if len(relative.parts) != 2 or relative.parts[1] != "admission.json":
        raise AdmissionError("admission path must be artifacts/admissions/<case-id>/admission.json")
    case_dir = root / relative.parts[0]
    reject_symlink_chain(case_dir, "admission case path")
    if not case_dir.is_dir():
        raise AdmissionError("admission case directory must be a real directory")

    schema = load_schema(ADMISSION_SCHEMA)
    record = load_object(admission_absolute, "existing admission")
    validate(record, schema, "existing admission")
    if record["frozen_request"]["case_id"] != relative.parts[0]:
        raise AdmissionError("existing admission case_id does not match its directory")
    if record["experiment_id"] != registration["experiment_id"]:
        raise AdmissionError("existing admission experiment_id mismatch")
    if record["registration_sha256"] != sha256_json(registration):
        raise AdmissionError("existing admission registration digest mismatch")
    admitted = utc_timestamp(record["admitted_at"], "admitted_at")
    request = record["frozen_request"]
    validate_request_semantics(request, registration, admitted)
    if record["request_sha256"] != sha256_json(request):
        raise AdmissionError("existing admission request digest mismatch")
    if record["comparability_sha256"] != sha256_json(request["comparability"]):
        raise AdmissionError("existing admission comparability digest mismatch")
    expected_assignment = {
        "condition": request["assignment"]["condition"],
        "mode": "explicit_preplanning_assignment",
        "automatic": False,
        "fairness_claim": "not_established_by_registration_v2",
        "registration_rule_status": "automatic_assignment_not_frozen",
    }
    rebuilt = build_record(request, registration, admitted, expected_assignment)
    if record != rebuilt:
        raise AdmissionError("existing admission semantic commitments do not match file truth")
    return record


def admit(
    registration_path: Path,
    request_path: Path,
    admissions_dir: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    reject_symlink_chain(registration_path, "registration path")
    registration = load_object(registration_path, "registration")
    admitted = (now or now_utc()).astimezone(timezone.utc)
    validate_registration(registration, registration_path, now=admitted)
    validate_active_registry_binding(registration_path, registration, now=admitted)
    admission_schema = load_schema(ADMISSION_SCHEMA)
    request = load_object(request_path, "admission request")
    validate(request, request_schema(admission_schema), "admission request")
    validate_request_semantics(request, registration, admitted)
    registration_digest = sha256_json(registration)
    request_digest = sha256_json(request)

    root = safe_admissions_root(registration_path, admissions_dir)
    lock_fd = _lock_fd(root)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        records = existing_records(root, admission_schema)
        case_id = request["case_id"]
        for path, existing in records:
            if existing["frozen_request"]["case_id"] != case_id:
                continue
            if existing["request_sha256"] == request_digest and existing["registration_sha256"] == registration_digest:
                return {
                    "status": "already_admitted",
                    "idempotent": True,
                    "admission_id": existing["admission_id"],
                    "case_id": case_id,
                    "condition": existing["assignment_evidence"]["condition"],
                    "automatic_assignment": existing["assignment_evidence"].get("automatic") is True,
                    "path": str(path),
                }
            raise AdmissionError("case_id already has an immutable conflicting admission")

        source = request["eligibility_evidence"]
        assignment = request["assignment"]
        for _path, existing in records:
            existing_source = existing["frozen_request"]["eligibility_evidence"]
            if source["ref"] == existing_source["ref"] or source["sha256"] == existing_source["sha256"]:
                raise AdmissionError("eligibility evidence is already bound to another case")
            existing_assignment = existing["frozen_request"]["assignment"]
            if "evidence_ref" in assignment and "evidence_ref" in existing_assignment and (assignment["evidence_ref"] == existing_assignment["evidence_ref"] or assignment["evidence_sha256"] == existing_assignment["evidence_sha256"]):
                raise AdmissionError("assignment evidence is already bound to another case")

        assignment_evidence = {
            "condition": assignment["condition"],
            "mode": "explicit_preplanning_assignment",
            "automatic": False,
            "fairness_claim": "not_established_by_registration_v2",
            "registration_rule_status": "automatic_assignment_not_frozen",
        }
        record = build_record(request, registration, admitted, assignment_evidence)
        validate(record, admission_schema, "admission record")

        case_dir = root / case_id
        if case_dir.exists() or case_dir.is_symlink():
            raise AdmissionError("case admission directory already exists")
        case_dir.mkdir(mode=0o700)
        try:
            path = case_dir / "admission.json"
            publish_create_only(path, record)
        except Exception:
            try:
                case_dir.rmdir()
            except OSError:
                pass
            raise
        _fsync_directory(root)
        return {
            "status": "admitted",
            "idempotent": False,
            "admission_id": record["admission_id"],
            "case_id": case_id,
            "condition": record["assignment_evidence"]["condition"],
            "automatic_assignment": record["assignment_evidence"].get("automatic") is True,
            "path": str(path),
        }
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registration", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument(
        "--admissions-dir",
        type=Path,
        help="defaults to <registration experiment>/artifacts/admissions",
    )
    args = parser.parse_args(argv)
    admissions_dir = args.admissions_dir or args.registration.parent / "artifacts/admissions"
    try:
        result = admit(args.registration, args.request, admissions_dir)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (AdmissionError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
