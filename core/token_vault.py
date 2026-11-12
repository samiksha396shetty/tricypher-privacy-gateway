"""Request-scoped token storage for reversible anonymization."""

from __future__ import annotations


class TokenVault:
    """Keep the original values needed to restore a single processed request."""

    def __init__(self) -> None:
        self._value_to_token: dict[tuple[str, str], str] = {}
        self._token_to_value: dict[str, str] = {}
        self._next_id: dict[str, int] = {}

    def token_for(self, entity_type: str, value: str) -> str:
        key = (entity_type, value)
        existing = self._value_to_token.get(key)
        if existing is not None:
            return existing

        index = self._next_id.get(entity_type, 0) + 1
        token = f"<{entity_type}_{index}>"
        self._next_id[entity_type] = index
        self._value_to_token[key] = token
        self._token_to_value[token] = value
        return token

    def restore(self, text: str) -> str:
        for token, value in self._token_to_value.items():
            text = text.replace(token, value)
        return text

    def __len__(self) -> int:
        return len(self._token_to_value)