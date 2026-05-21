from dataclasses import dataclass

from office365.runtime.client_value_collection import ClientValueCollection


@dataclass(init=False)
class FieldMultiChoiceValue(ClientValueCollection[str]):
    """A collection of choice values."""

    def __init__(self, initial_values=None):
        super().__init__(str, initial_values)
