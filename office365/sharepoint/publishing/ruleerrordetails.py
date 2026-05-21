from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.publishing.error import Error


@dataclass
class RuleErrorDetails(ClientValue):
    errorHeaders: StringCollection = field(default_factory=StringCollection)
    errors: Error = field(default_factory=lambda: Error())

    @property
    def entity_type_name(self):
        return "SP.Publishing.RuleErrorDetails"
