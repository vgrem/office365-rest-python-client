from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteDesignImage(ClientValue):
    def __init__(self, display_name: Optional[str] = None, image_url: Optional[str] = None):
        self.DisplayName = display_name
        self.ImageUrl = image_url

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignImage"
