from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class Error(ClientValue):
    Details: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "SP.Publishing.Error"
