from office365.runtime.client_value_collection import ClientValueCollection


class FieldMultiChoiceValue(ClientValueCollection[str]):
    """A collection of choice values."""

    def __init__(self, initial_values=None):
        super().__init__(str, initial_values)
