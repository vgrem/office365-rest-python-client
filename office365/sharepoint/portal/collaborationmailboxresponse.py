from office365.runtime.client_value import ClientValue
from typing import Optional


class CollaborationMailboxResponse(ClientValue):
    def __init__(
        self,
        alternate_url: Optional[str] = None,
        correlation_id: Optional[str] = None,
        error_code: Optional[int] = None,
        status: Optional[int] = None,
        url: Optional[str] = None,
    ):
        self.AlternateUrl = alternate_url
        self.CorrelationId = correlation_id
        self.ErrorCode = error_code
        self.Status = status
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.CollaborationMailboxResponse"
