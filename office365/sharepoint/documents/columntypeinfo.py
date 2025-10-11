from office365.runtime.client_value import ClientValue


class ColumnTypeInfo(ClientValue):

    def __init__(self, placeholder_id: str = None, translated_placeholder_type: str = None):
        self.placeholder_id = placeholder_id
        self.translated_placeholder_type = translated_placeholder_type
