from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.portallaunch.wave import PortalLaunchWave


class PortalLaunchWaveSetup(ClientValue):

    def __init__(
        self,
        alternative_urls_of_new_site: str = None,
        alternative_urls_of_old_site: str = None,
        created_on: datetime = None,
        expected_users_size: int = None,
        is_paused: bool = None,
        modified_on: datetime = None,
        new_site_url: str = None,
        owners_and_editors: dict = None,
        pause_at_wave: int = None,
        redirection_type: int = None,
        redirect_url: str = None,
        site_id: str = None,
        status: int = None,
        wave_override_users: str = None,
        waves: ClientValueCollection[PortalLaunchWave] = ClientValueCollection(
            PortalLaunchWave
        ),
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
