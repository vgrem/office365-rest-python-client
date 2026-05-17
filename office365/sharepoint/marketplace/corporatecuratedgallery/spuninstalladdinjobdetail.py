from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spuninstalladdinerrordetail import (
    SPUninstallAddinErrorDetail,
)


class SPUninstallAddinJobDetail(ClientValue):
    def __init__(
        self,
        absolute_url: Optional[str] = None,
        app_instance_id: Optional[str] = None,
        error_details: ClientValueCollection[SPUninstallAddinErrorDetail] = ClientValueCollection(
            SPUninstallAddinErrorDetail
        ),
        job_id: Optional[str] = None,
        server_relative_url: Optional[str] = None,
        site_id: Optional[str] = None,
        task_start_time: Optional[datetime] = None,
    ):
        self.absoluteUrl = absolute_url
        self.appInstanceId = app_instance_id
        self.errorDetails = error_details
        self.jobId = job_id
        self.serverRelativeUrl = server_relative_url
        self.siteId = site_id
        self.taskStartTime = task_start_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinJobDetail"
