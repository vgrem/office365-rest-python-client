from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection
from typing import Optional


class HomeSiteConfigurationParam(ClientValue):
    def __init__(
        self,
        audiences: GuidCollection = GuidCollection(),
        is_audiences_present: Optional[bool] = None,
        is_go_back_to_connections_button_disabled: Optional[bool] = None,
        is_in_draft_mode: Optional[bool] = None,
        is_in_draft_mode_present: Optional[bool] = None,
        is_order_present: Optional[bool] = None,
        is_targeted_license_type_present: Optional[bool] = None,
        is_viva_backend_site: Optional[bool] = None,
        is_viva_backend_site_present: Optional[bool] = None,
        is_viva_connections_default_start_present: Optional[bool] = None,
        order: Optional[int] = None,
        targeted_license_type: Optional[int] = None,
        viva_connections_default_start: Optional[bool] = None,
    ):
        self.Audiences = audiences
        self.IsAudiencesPresent = is_audiences_present
        self.isGoBackToConnectionsButtonDisabled = is_go_back_to_connections_button_disabled
        self.isInDraftMode = is_in_draft_mode
        self.IsInDraftModePresent = is_in_draft_mode_present
        self.IsOrderPresent = is_order_present
        self.IsTargetedLicenseTypePresent = is_targeted_license_type_present
        self.IsVivaBackendSite = is_viva_backend_site
        self.IsVivaBackendSitePresent = is_viva_backend_site_present
        self.IsVivaConnectionsDefaultStartPresent = is_viva_connections_default_start_present
        self.Order = order
        self.TargetedLicenseType = targeted_license_type
        self.vivaConnectionsDefaultStart = viva_connections_default_start

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.PortalAndOrgNews.HomeSiteConfigurationParam"
