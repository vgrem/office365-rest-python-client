from office365.runtime.client_value import ClientValue


class SPTriggeredUninstallAddinJobResponse(ClientValue):
    def __init__(
        self,
        absolute_url: str = None,
        app_instance_id: str = None,
        server_relative_url: str = None,
        uninstall_job_id: str = None,
    ):
        self.absoluteUrl = absolute_url
        self.appInstanceId = app_instance_id
        self.serverRelativeUrl = server_relative_url
        self.uninstallJobId = uninstall_job_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTriggeredUninstallAddinJobResponse"
