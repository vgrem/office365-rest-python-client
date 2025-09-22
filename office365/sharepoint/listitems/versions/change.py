from office365.runtime.client_value import ClientValue


class SPListItemVersionChange(ClientValue):

    def __init__(
        self, field_title: str = None, new_value: str = None, previous_value: str = None
    ):
        self.field_title = field_title
        self.new_value = new_value
        self.previous_value = previous_value
