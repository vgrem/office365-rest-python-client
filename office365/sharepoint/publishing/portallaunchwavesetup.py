from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.portallaunch.wave import PortalLaunchWave


class PortalLaunchWaveSetup(ClientValue):
    def __init__(
        self,
        alternative_urls_of_new_site: Optional[str] = None,
        alternative_urls_of_old_site: Optional[str] = None,
        created_on: Optional[datetime] = None,
        expected_users_size: Optional[int] = None,
        is_paused: Optional[bool] = None,
        modified_on: Optional[datetime] = None,
        new_site_url: Optional[str] = None,
        owners_and_editors: Optional[dict] = None,
        pause_at_wave: Optional[int] = None,
        redirection_type: Optional[int] = None,
        redirect_url: Optional[str] = None,
        site_id: Optional[str] = None,
        status: Optional[int] = None,
        wave_override_users: Optional[str] = None,
        waves: ClientValueCollection[PortalLaunchWave] = ClientValueCollection(PortalLaunchWave),
    ):
        self.AlternativeUrlsOfNewSite = alternative_urls_of_new_site
        self.AlternativeUrlsOfOldSite = alternative_urls_of_old_site
        self.CreatedOn = created_on
        self.ExpectedUsersSize = expected_users_size
        self.IsPaused = is_paused
        self.ModifiedOn = modified_on
        self.NewSiteUrl = new_site_url
        self.OwnersAndEditors = owners_and_editors
        self.PauseAtWave = pause_at_wave
        self.RedirectionType = redirection_type
        self.RedirectUrl = redirect_url
        self.SiteId = site_id
        self.Status = status
        self.WaveOverrideUsers = wave_override_users
        self.Waves = waves

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWaveSetup"
