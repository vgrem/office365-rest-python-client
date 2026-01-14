from office365.directory.authentication.fido2restrictionenforcementtype import Fido2RestrictionEnforcementType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class Fido2KeyRestrictions(ClientValue):
    def __init__(
        self,
        aa_guids: StringCollection = None,
        enforcement_type: Fido2RestrictionEnforcementType = Fido2RestrictionEnforcementType.none,
        is_enforced: bool = None,
    ):
        self.aaGuids = aa_guids
        self.enforcementType = enforcement_type
        self.isEnforced = is_enforced

    @property
    def entity_type_name(self):
        return "microsoft.graph.Fido2KeyRestrictions"
