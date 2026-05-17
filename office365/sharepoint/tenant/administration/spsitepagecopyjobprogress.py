from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPSitePageCopyJobProgress(ClientValue):
    def __init__(
        self,
        error_message: Optional[str] = None,
        job_state: Optional[str] = None,
        new_page_url: Optional[str] = None,
        source_page_name: Optional[str] = None,
        status_message: Optional[str] = None,
        work_item_id: Optional[UUID] = None,
    ):
        self.ErrorMessage = error_message
        self.JobState = job_state
        self.NewPageUrl = new_page_url
        self.SourcePageName = source_page_name
        self.StatusMessage = status_message
        self.WorkItemId = work_item_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePageCopyJobProgress"
