"""AC-05 fail-closed context disclosure policy for agent consultations.

Only explicitly approved field names can be exported; secret-bearing fields
are denied even when an erroneous allowlist includes them.
"""
from __future__ import annotations
import re

SENSITIVE = re.compile(
    r"(secret|password|token|api[_-]?key|credential|private[_-]?key|"
    r"unpublished|confidential|manuscript|patient|personal|raw[_-]?data|"
    r"access[_-]?key|authorization)",
    re.IGNORECASE,
)
SAFE_FIELDS = frozenset({"task_id", "objective", "public_context", "constraints",
                         "review_question", "evidence_refs", "deadline"})
CLASSIFICATIONS = frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"})

def export_context(context: dict, recipient: str, *, classification: str,
                   approved_fields: list[str] | None = None,
                   guest: bool = False, guest_approved: bool = False) -> dict:
    """Build a minimal outbound payload; does not perform transmission.

    Any non-public classification is blocked from guest recipients.
    INTERNAL context requires explicit field-level approval for specialists.
    CONFIDENTIAL and RESTRICTED data never leave this boundary.
    """
    if not isinstance(context, dict) or not isinstance(recipient, str) or not recipient.strip():
        raise ValueError("Invalid context or recipient")
    if classification not in CLASSIFICATIONS:
        raise ValueError("Unknown classification")
    if classification in {"CONFIDENTIAL", "RESTRICTED"}:
        raise PermissionError("Sensitive task context cannot be exported")
    if guest and (not guest_approved or classification != "PUBLIC"):
        raise PermissionError("Guest disclosure requires explicit approval and PUBLIC context")
    if not isinstance(approved_fields, list) or not all(isinstance(x, str) for x in approved_fields):
        raise PermissionError("Explicit field allowlist required")
    if any(k not in SAFE_FIELDS or SENSITIVE.search(k) for k in approved_fields):
        raise PermissionError("Field not eligible for disclosure")
    if any(k not in context for k in approved_fields):
        raise ValueError("Approved field missing from context")
    payload = {}
    for key in approved_fields:
        value = context[key]
        if not isinstance(value, (str, int, float, bool, list)):
            raise PermissionError("Unsupported payload type")
        if isinstance(value, list) and not all(isinstance(v, str) for v in value):
            raise PermissionError("Only string evidence references permitted")
        if isinstance(value, str) and SENSITIVE.search(value):
            raise PermissionError("Potentially sensitive text; human redaction required")
        if isinstance(value, list) and any(SENSITIVE.search(v) for v in value):
            raise PermissionError("Potentially sensitive reference; human redaction required")
        payload[key] = value
    return {"recipient": recipient, "classification": classification,
            "guest": guest, "payload": payload, "transmitted": False}
