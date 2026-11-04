from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class SPAddinPermissionRequest(ClientValue):
    appIdentifiers: StringCollection = field(default_factory=StringCollection)
    serverRelativeUrl: Optional[str] = None
    url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionRequest"
