from enum import Enum


class ExternalAudienceScope(Enum):
    none = "0"
    contactsOnly = "1"
    all = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ExternalAudienceScope"
