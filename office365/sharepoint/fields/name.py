from __future__ import annotations

import re


def internal_field_name(name: str) -> str:
    """Sanitize a display/column name into a SharePoint field internal name.

    SharePoint field internal names cannot contain spaces or punctuation.
    """
    return re.sub(r"\W", "_", name)
