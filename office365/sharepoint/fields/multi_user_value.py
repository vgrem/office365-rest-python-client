from dataclasses import dataclass

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.fields.user_value import FieldUserValue


@dataclass(init=False)
class FieldMultiUserValue(ClientValueCollection[FieldUserValue]):
    """Represents the multi valued user field for a list item."""

    def __init__(self, initial_values=None):
        super().__init__(FieldUserValue, initial_values)
