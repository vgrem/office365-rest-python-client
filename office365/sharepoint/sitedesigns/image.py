from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteDesignImage(ClientValue):
    DisplayName: Optional[str] = None
    ImageUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignImage"
