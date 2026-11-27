"""Council workspace with explicit local export and validated replay. No execution or network."""
import json
from pathlib import Path
from copy import deepcopy
from agent_council import council, review, decide

from agent_confidentiality import export_context
from agent_review_provenance import assess_submission
from agent_repair_gate import assess_repair

class CouncilWorkspace:
    def __init__(self):
        self._record = None

    def snapshot(self):
        return deepcopy(self._record)

    def convene(self, task):
        if self._record is not None:
            raise ValueError("Workspace already contains a council")
        self._record = council(deepcopy(task))
        return self.snapshot()

    def submit_review(self, entry):
        if self._record is None:
            raise ValueError("Convene a council first")
        self._record = review(self.snapshot(), deepcopy(entry))
        return self.snapshot()

    def human_decision(self, decision, rationale):
        if self._record is None:
            raise ValueError("Convene a council first")
        self._record = decide(self.snapshot(), decision, rationale)
        return self.snapshot()

    def prepare_consultation(self, recipient, *, classification, approved_fields):
        if self._record is None:
            raise ValueError("Convene a council first")
        context = {"task_id": self._record["task_id"], "objective": self._record["summary"]}
        return export_context(context, recipient, classification=classification,
                              approved_fields=approved_fields, guest=True, guest_approved=False)

    def audit_review_receipt(self, entry):
        if self._record is None or entry.get("task_id") != self._record["task_id"]:
            raise ValueError("Review does not belong to current task")
        return assess_submission(entry, trusted_runs={})

    def audit_repair(self, record):
        if self._record is None or record.get("task_id") != self._record["task_id"]:
            raise ValueError("Repair does not belong to current task")
        safe = deepcopy(record)
        safe["trusted_runner_verified"] = False
        return assess_repair(safe)

    def export(self, path):
        if self._record is None:
            raise ValueError("No council to export")
        with Path(path).open("x", encoding="utf-8") as stream:
            json.dump(self.snapshot(), stream, ensure_ascii=False, indent=2)

    def restore(self, path):
        if self._record is not None:
            raise ValueError("Workspace already contains a council")
        with Path(path).open("rb") as stream:
            raw = stream.read(1048577)
        if len(raw) > 1048576:
            raise ValueError("Session exceeds size limit")
        saved = json.loads(raw)
        if not isinstance(saved, dict):
            raise ValueError("Invalid session")
        rebuilt = CouncilWorkspace()
        rebuilt.convene({"id":saved["task_id"], "summary":saved["summary"],
                         "specialties":saved["specialties"], "guests":saved["guest_advisers"]})
        for entry in saved["reviews"]:
            rebuilt.submit_review(entry)
        if saved["human_decision"] != "PENDING":
            rebuilt.human_decision(saved["human_decision"].lower(), saved["human_rationale"])
        if rebuilt.snapshot() != saved:
            raise ValueError("Session differs from validated replay")
        self._record = rebuilt.snapshot()
        return self.snapshot()
