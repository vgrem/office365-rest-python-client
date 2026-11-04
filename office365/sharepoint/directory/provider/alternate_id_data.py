from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AlternateIdData(ClientValue):
    Email: Optional[str] = None
    IdentifyingProperty: Optional[str] = None
    UserPrincipalName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.AlternateIdData"
