from typing import Optional

from office365.runtime.client_value import ClientValue


class OutOfBoxSiteTemplateSettings(ClientValue):
    def __init__(self, id_: Optional[str] = None, is_hidden: Optional[bool] = None):
        self.Id = id_
        self.IsHidden = is_hidden

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.OutOfBoxSiteTemplateSettings"
