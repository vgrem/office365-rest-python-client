from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SPACSServicePrincipalInfo(ClientValue):

    ApplicationEndpointAuthorities: StringCollection | None = None
    DisplayName = None
    appDomains: Optional[StringCollection] = None
    appId: Optional[str] = None
    appIdentifier: Optional[str] = None
    redirectUri: Optional[str] = None
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Authentication.SPACSServicePrincipalInfo"