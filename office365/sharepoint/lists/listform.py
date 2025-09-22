from office365.runtime.client_value import ClientValue


class ListForm(ClientValue):

    def __init__(
        self, has_source_field: bool = None, id_: str = None, schema_json: str = None
    ):
        self.has_source_field = has_source_field
        self.id = id_
        self.schema_json = schema_json
