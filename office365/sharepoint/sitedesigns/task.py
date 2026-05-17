from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteDesignTask(ClientValue):
    def __init__(
        self,
        id_: Optional[str] = None,
        logon_name: Optional[str] = None,
        site_design_id: Optional[str] = None,
        site_design_store: Optional[int] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.ID = id_
        self.LogonName = logon_name
        self.SiteDesignID = site_design_id
        self.SiteDesignStore = site_design_store
        self.SiteID = site_id
        self.WebID = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignTask"
