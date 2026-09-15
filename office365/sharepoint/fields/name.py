from __future__ import annotations

import re

# Built-in SharePoint field titles that collide with a user column of the same
# name. ``FieldCollection.ensure`` looks fields up by *display name*
# (``getByTitle``), so a column titled e.g. "Name" resolves to the built-in
# ``FileLeafRef`` field and is never created as a custom column. Such titles are
# suffixed with ``_`` so the column can be imported (and the item keys stay
# consistent, since both field creation and record keys use this mapping).
_RESERVED_FIELD_TITLES = frozenset(
    {
        "name",  # FileLeafRef
        "title",
        "id",
        "created",
        "modified",
        "author",
        "editor",
        "attachments",
        "contenttype",
        "contenttypeid",
        "version",
        "uniqueid",
        "fileleafref",
        "fileref",
        "filedirref",
        "fsobjtype",
        "owshiddenversion",
        "workflowversion",
        "metainfo",
        "scopeid",
        "instanceid",
        "permask",
    }
)


def internal_field_name(name: str) -> str:
    """Sanitize a display/column name into a SharePoint field internal name.

    SharePoint field internal names cannot contain spaces or punctuation, and a
    title that collides with a built-in field's display name (e.g. ``Name`` ->
    ``FileLeafRef``) cannot be created as a custom column — those are suffixed
    with ``_`` so the import still works.
    """
    sanitized = re.sub(r"\W", "_", name)
    if sanitized.lower() in _RESERVED_FIELD_TITLES:
        return f"{sanitized}_"
    return sanitized


def is_reserved_field_title(name: str) -> bool:
    """Whether a column title collides with a built-in SharePoint field title."""
    return re.sub(r"\W", "_", name).lower() in _RESERVED_FIELD_TITLES
