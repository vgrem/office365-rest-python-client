"""Helpers for building OData literals safely."""

from __future__ import annotations


def escape_odata_string(value: str) -> str:
    """Escape a string for use inside an OData ``'...'`` literal.

    Both OData v3 (SharePoint) and v4 (Microsoft Graph) escape an embedded
    single quote by doubling it, so ``O'Brien`` becomes ``O''Brien`` when used
    in a filter such as ``displayName eq 'O''Brien'``.

    Args:
        value: The raw string value.

    Returns:
        The escaped value, safe to embed between single quotes.
    """
    return value.replace("'", "''")
