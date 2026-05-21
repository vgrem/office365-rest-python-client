from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class HomeSitesDetails(ClientValue):
    Audiences: StringCollection = field(default_factory=StringCollection)
    IsInDraftMode: Optional[bool] = None
    Title: Optional[str] = None
    Url: Optional[str] = None
    WebId: Optional[str] = None
    IsVivaBackendSite: Optional[bool] = None
    MatchingAudiences: StringCollection = field(default_factory=StringCollection)
    SiteId: Optional[str] = None
    TargetedLicenseType: Optional[int] = None
    VivaConnectionsDefaultStart: Optional[bool] = None
