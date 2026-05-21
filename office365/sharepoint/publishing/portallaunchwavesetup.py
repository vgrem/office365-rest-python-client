from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.portallaunch.wave import PortalLaunchWave


@dataclass
class PortalLaunchWaveSetup(ClientValue):
    AlternativeUrlsOfNewSite: Optional[str] = None
    AlternativeUrlsOfOldSite: Optional[str] = None
    CreatedOn: Optional[datetime] = None
    ExpectedUsersSize: Optional[int] = None
    IsPaused: Optional[bool] = None
    ModifiedOn: Optional[datetime] = None
    NewSiteUrl: Optional[str] = None
    OwnersAndEditors: dict = field(default_factory=dict)
    PauseAtWave: Optional[int] = None
    RedirectionType: Optional[int] = None
    RedirectUrl: Optional[str] = None
    SiteId: Optional[str] = None
    Status: Optional[int] = None
    WaveOverrideUsers: Optional[str] = None
    Waves: ClientValueCollection[PortalLaunchWave] = field(
        default_factory=lambda: ClientValueCollection(PortalLaunchWave)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWaveSetup"
