from office365.runtime.client_value import ClientValue


class SiteDesignTask(ClientValue):

    def __init__(
        self,
        id_: str = None,
        logon_name: str = None,
        site_design_id: str = None,
        site_design_store: int = None,
        site_id: str = None,
        web_id: str = None,
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
