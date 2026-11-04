from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPErrorWithServerRelativeUrl(ClientValue):
    errorMessage: Optional[str] = None
    serverRelativeUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPErrorWithServerRelativeUrl"
