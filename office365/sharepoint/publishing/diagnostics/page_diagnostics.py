from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.diagnostics.page_result import (
    PageDiagnosticsResult,
)


class PageDiagnostics(ClientValue):
    def __init__(
        self,
        results=None,
        latest_draft_version: str = None,
        latest_published_version: str = None,
        page_file_name: str = None,
    ):
        self.Results = ClientValueCollection(PageDiagnosticsResult, results)
        self.LatestDraftVersion = latest_draft_version
        self.LatestPublishedVersion = latest_published_version
        self.PageFileName = page_file_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDiagnostics"
