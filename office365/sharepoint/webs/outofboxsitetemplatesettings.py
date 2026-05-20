from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class OutOfBoxSiteTemplateSettings(ClientValue):
    Id: Optional[str] = None
    IsHidden: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.OutOfBoxSiteTemplateSettings"
