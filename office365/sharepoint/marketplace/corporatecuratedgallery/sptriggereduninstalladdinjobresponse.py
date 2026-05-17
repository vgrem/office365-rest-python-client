from typing import Optional

from office365.runtime.client_value import ClientValue


class SPTriggeredUninstallAddinJobResponse(ClientValue):
    def __init__(
        self,
        absolute_url: Optional[str] = None,
        app_instance_id: Optional[str] = None,
        server_relative_url: Optional[str] = None,
        uninstall_job_id: Optional[str] = None,
    ):
        self.absoluteUrl = absolute_url
        self.appInstanceId = app_instance_id
        self.serverRelativeUrl = server_relative_url
        self.uninstallJobId = uninstall_job_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTriggeredUninstallAddinJobResponse"
