from office365.runtime.client_value import ClientValue


class ListForm(ClientValue):

    def __init__(self, has_source_field: bool = None, id_: str = None, schema_json: str = None):
        self.HasSourceField = has_source_field
        self.Id = id_
        self.SchemaJSON = schema_json
