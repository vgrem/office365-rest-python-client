from office365.runtime.client_value import ClientValue


class SPFailToTriggerUninstallAddinJobResponse(ClientValue):
    def __init__(
        self,
        app_instance_id: str = None,
        error_message: str = None,
        server_relative_url: str = None,
    ):
        self.appInstanceId = app_instance_id
        self.errorMessage = error_message
        self.serverRelativeUrl = server_relative_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPFailToTriggerUninstallAddinJobResponse"
