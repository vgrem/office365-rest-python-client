from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class Error(ClientValue):
    Details: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "SP.Publishing.Error"
