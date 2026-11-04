from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AutofillColumnInfo(ClientValue):
    ColumnDataType: Optional[str] = None
    columnName: Optional[str] = None
    isEnabled: Optional[bool] = None
    prompt: Optional[str] = None
    preventOverwrite: bool | None = None
    overwriteMode: int | None = None
    processingPass: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.AutofillColumnInfo"
