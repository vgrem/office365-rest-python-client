from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPSitePageCopyJobProgress(ClientValue):

    def __init__(
        self,
        error_message: str = None,
        job_state: str = None,
        new_page_url: str = None,
        source_page_name: str = None,
        status_message: str = None,
        work_item_id: UUID = None,
    ):
        self.ErrorMessage = error_message
        self.JobState = job_state
        self.NewPageUrl = new_page_url
        self.SourcePageName = source_page_name
        self.StatusMessage = status_message
        self.WorkItemId = work_item_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePageCopyJobProgress"
