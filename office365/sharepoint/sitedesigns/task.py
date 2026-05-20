from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteDesignTask(ClientValue):
    ID: Optional[str] = None
    LogonName: Optional[str] = None
    SiteDesignID: Optional[str] = None
    SiteDesignStore: Optional[int] = None
    SiteID: Optional[str] = None
    WebID: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignTask"
