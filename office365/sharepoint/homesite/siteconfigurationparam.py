from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class HomeSiteConfigurationParam(ClientValue):

    def __init__(
        self,
        audiences: GuidCollection = GuidCollection(),
        is_audiences_present: bool = None,
        is_go_back_to_connections_button_disabled: bool = None,
        is_in_draft_mode: bool = None,
        is_in_draft_mode_present: bool = None,
        is_order_present: bool = None,
        is_targeted_license_type_present: bool = None,
        is_viva_backend_site: bool = None,
        is_viva_backend_site_present: bool = None,
        is_viva_connections_default_start_present: bool = None,
        order: int = None,
        targeted_license_type: int = None,
        viva_connections_default_start: bool = None,
    ):
        self.Audiences = audiences
        self.IsAudiencesPresent = is_audiences_present
        self.isGoBackToConnectionsButtonDisabled = (
            is_go_back_to_connections_button_disabled
        )
        self.isInDraftMode = is_in_draft_mode
        self.IsInDraftModePresent = is_in_draft_mode_present
        self.IsOrderPresent = is_order_present
        self.IsTargetedLicenseTypePresent = is_targeted_license_type_present
        self.IsVivaBackendSite = is_viva_backend_site
        self.IsVivaBackendSitePresent = is_viva_backend_site_present
        self.IsVivaConnectionsDefaultStartPresent = (
            is_viva_connections_default_start_present
        )
        self.Order = order
        self.TargetedLicenseType = targeted_license_type
        self.vivaConnectionsDefaultStart = viva_connections_default_start

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.PortalAndOrgNews.HomeSiteConfigurationParam"
