from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class HomeSiteConfigurationParam(ClientValue):
    Audiences: GuidCollection = field(default_factory=GuidCollection)
    IsAudiencesPresent: Optional[bool] = None
    isGoBackToConnectionsButtonDisabled: Optional[bool] = None
    isInDraftMode: Optional[bool] = None
    IsInDraftModePresent: Optional[bool] = None
    IsOrderPresent: Optional[bool] = None
    IsTargetedLicenseTypePresent: Optional[bool] = None
    IsVivaBackendSite: Optional[bool] = None
    IsVivaBackendSitePresent: Optional[bool] = None
    IsVivaConnectionsDefaultStartPresent: Optional[bool] = None
    Order: Optional[int] = None
    TargetedLicenseType: Optional[int] = None
    vivaConnectionsDefaultStart: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.PortalAndOrgNews.HomeSiteConfigurationParam"
