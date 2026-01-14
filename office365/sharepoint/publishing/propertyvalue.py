from office365.runtime.client_value import ClientValue


class PropertyValue(ClientValue):
    def __init__(self, term_id: str = None, value: str = None):
        self.TermId = term_id
        self.Value = value

    @property
    def entity_type_name(self):
        return "SP.Publishing.PropertyValue"
