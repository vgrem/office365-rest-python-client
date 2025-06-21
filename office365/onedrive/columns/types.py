from enum import Enum


class ColumnTypes(Enum):
    text = "text"
    """Single line text."""

    note = "note"
    """Multiline text."""

    choice = "choice"
    """Choice column"""

    multichoice = "multichoice"
    """Multichoice column."""
