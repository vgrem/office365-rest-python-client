from office365.runtime.client_value import ClientValue


class ColumnDef(ClientValue):

    def __init__(
        self,
        custom_formatter: str = None,
        id_: str = None,
        name: str = None,
        type_: str = None,
    ):
        self.CustomFormatter = custom_formatter
        self.Id = id_
        self.Name = name
        self.Type = type_
