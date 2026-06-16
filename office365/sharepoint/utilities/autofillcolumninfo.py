from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AutofillColumnInfo(ClientValue):
    ColumnDataType: Optional[str] = None
    columnName: Optional[str] = None
    isEnabled: Optional[bool] = None
    prompt: Optional[str] = None
    preventOverwrite: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.AutofillColumnInfo"
