from enum import Enum


class ViewScope(Enum):
    """Specifies the scope for returning list items and list folders in a list view."""

    DefaultValue = "DefaultValue"

    Recursive = "Recursive"
    """Shows all files in the specified folder or any folder descending from it."""

    RecursiveAll = "RecursiveAll"
    """Shows all files and folders in the specified folder or any folder descending from it"""

    FilesOnly = "FilesOnly"
    """Shows only the files in the specified folder. """
