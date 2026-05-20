from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class WorkbookWorksheetProtectionOptions(ClientValue):
    """Represents the protection of a sheet object."""

    allowAutoFilter: bool | None = None
    allowDeleteColumns: bool | None = None
    allowDeleteRows: bool | None = None
    allowFormatCells: bool | None = None
    allowFormatColumns: bool | None = None
    allowFormatRows: bool | None = None
    allowInsertColumns: bool | None = None
    allowInsertHyperlinks: bool | None = None
    allowInsertRows: bool | None = None
    allowPivotTables: bool | None = None
    allowSort: bool | None = None
