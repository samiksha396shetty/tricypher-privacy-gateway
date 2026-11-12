"""Restore request-scoped tokens in a response."""

from core.token_vault import TokenVault


def restore_tokens(text: str, vault: TokenVault) -> str:
    """Replace known placeholders with their original values."""
    return vault.restore(text)
