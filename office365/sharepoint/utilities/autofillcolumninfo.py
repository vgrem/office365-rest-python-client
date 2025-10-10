from office365.runtime.client_value import ClientValue


class AutofillColumnInfo(ClientValue):

    def __init__(
        self,
        column_data_type: str = None,
        column_name: str = None,
        is_enabled: bool = None,
        prompt: str = None,
    ):
        self.ColumnDataType = column_data_type
        self.columnName = column_name
        self.isEnabled = is_enabled
        self.prompt = prompt

    @property
    def entity_type_name(self):
        return "SP.Utilities.AutofillColumnInfo"
