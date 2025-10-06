from office365.runtime.client_value import ClientValue


class CardDesignFeatures(ClientValue):

    def __init__(
        self,
        catalog_type: int = None,
        is_context_not_available: bool = None,
        is_disabled_by_tenant_admin: bool = None,
        is_enabled: bool = None,
        is_flight_deactivated: bool = None,
        is_not_a_home_site: bool = None,
    ):
        self.catalogType = catalog_type
        self.isContextNotAvailable = is_context_not_available
        self.isDisabledByTenantAdmin = is_disabled_by_tenant_admin
        self.isEnabled = is_enabled
        self.isFlightDeactivated = is_flight_deactivated
        self.isNotAHomeSite = is_not_a_home_site

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesignFeatures"
