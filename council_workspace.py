"""In-memory council workspace. No execution, network or filesystem writes."""
from copy import deepcopy
from agent_council import council, review, decide

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
