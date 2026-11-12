"""Project-specific patterns and validation functions."""

from detection.validators import is_valid_api_key, is_valid_employee_id

CUSTOM_RECOGNIZERS = (
    {
        "entity_type": "API_KEY",
        "pattern": r"\b(?:sk-[A-Za-z0-9_-]{20,}|api_[A-Za-z0-9_-]{20,})\b",
        "validator": is_valid_api_key,
        "score": 0.98,
    },
    {
        "entity_type": "EMPLOYEE_ID",
        "pattern": r"\bEMP-\d{4,8}\b",
        "validator": is_valid_employee_id,
        "score": 0.90,
    },
)
