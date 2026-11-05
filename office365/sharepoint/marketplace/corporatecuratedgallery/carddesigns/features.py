from typing import Optional

from office365.runtime.client_value import ClientValue


class CardDesignFeatures(ClientValue):
    catalogType: Optional[int] = None
    isContextNotAvailable: Optional[bool] = None
    isDisabledByTenantAdmin: Optional[bool] = None
    isEnabled: Optional[bool] = None
    isFlightDeactivated: Optional[bool] = None
    isNotAHomeSite: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesignFeatures"
