from office365.runtime.client_value import ClientValue


class OutOfBoxSiteTemplateSettings(ClientValue):
    def __init__(self, id_: str = None, is_hidden: bool = None):
        self.Id = id_
        self.IsHidden = is_hidden

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.OutOfBoxSiteTemplateSettings"
