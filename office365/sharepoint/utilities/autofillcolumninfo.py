from office365.runtime.client_value import ClientValue
from typing import Optional


class AutofillColumnInfo(ClientValue):
    def __init__(
        self,
        column_data_type: Optional[str] = None,
        column_name: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        prompt: Optional[str] = None,
    ):
        self.ColumnDataType = column_data_type
        self.columnName = column_name
        self.isEnabled = is_enabled
        self.prompt = prompt

    @property
    def entity_type_name(self):
        return "SP.Utilities.AutofillColumnInfo"
