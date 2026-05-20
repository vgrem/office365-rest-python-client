from __future__ import annotations

from dataclasses import dataclass

from office365.directory.authentication.fido2restrictionenforcementtype import Fido2RestrictionEnforcementType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class Fido2KeyRestrictions(ClientValue):
    aaGuids: StringCollection | None = None
    enforcementType: Fido2RestrictionEnforcementType = Fido2RestrictionEnforcementType.none
    isEnforced: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Fido2KeyRestrictions"
