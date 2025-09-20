from office365.runtime.client_value import ClientValue


class CAFieldValue(ClientValue):

    def __init__(
        self,
        data_type: str = None,
        id_: str = None,
        name: str = None,
        value: str = None,
    ):
        self.data_type = data_type
        self.id = id_
        self.name = name
        self.value = value
