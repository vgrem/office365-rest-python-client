from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.audit.search_request_status import (
    AuditSearchRequestStatus,
)


class PageResponse(ClientValue):

    def __init__(
        self,
        continuation_token: str = None,
        page_number: int = None,
        page_result: ClientValueCollection[
            AuditSearchRequestStatus
        ] = ClientValueCollection(AuditSearchRequestStatus),
        page_size: int = None,
        total_count: int = None,
        total_pages: int = None,
    ):
        self.ContinuationToken = continuation_token
        self.PageNumber = page_number
        self.PageResult = page_result
        self.PageSize = page_size
        self.TotalCount = total_count
        self.TotalPages = total_pages

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.PageResponse"
