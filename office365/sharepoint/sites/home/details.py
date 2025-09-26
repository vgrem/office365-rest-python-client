from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class HomeSitesDetails(ClientValue):

    def __init__(
        self,
        audiences=None,
        is_in_draft_mode=None,
        title=None,
        url=None,
        web_id=None,
        is_viva_backend_site: bool = None,
        matching_audiences: StringCollection = StringCollection(),
        site_id: str = None,
        targeted_license_type: int = None,
        viva_connections_default_start: bool = None,
    ):
        """
        :param list[str] audiences:
        :param bool is_in_draft_mode:
        :param str title:
        :param str url:
        :param str web_id:
        """
        self.Audiences = StringCollection(audiences)
        self.IsInDraftMode = is_in_draft_mode
        self.Title = title
        self.Url = url
        self.WebId = web_id
        self.IsVivaBackendSite = is_viva_backend_site
        self.MatchingAudiences = matching_audiences
        self.SiteId = site_id
        self.TargetedLicenseType = targeted_license_type
        self.VivaConnectionsDefaultStart = viva_connections_default_start
