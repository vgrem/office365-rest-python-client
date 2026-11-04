from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.fields.lookup_value import FieldLookupValue


@value
class FieldMultiLookupValue(ClientValueCollection[FieldLookupValue]):
    """A collection of FieldLookupValue items."""

    def __init__(self, initial_values=None):
        super().__init__(FieldLookupValue, initial_values)
