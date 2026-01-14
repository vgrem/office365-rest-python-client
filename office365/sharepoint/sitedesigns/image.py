from office365.runtime.client_value import ClientValue


class SiteDesignImage(ClientValue):
    def __init__(self, display_name: str = None, image_url: str = None):
        self.DisplayName = display_name
        self.ImageUrl = image_url

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignImage"
