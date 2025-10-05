from office365.runtime.client_value import ClientValue


class CollaborationMailboxResponse(ClientValue):

    def __init__(
        self,
        alternate_url: str = None,
        correlation_id: str = None,
        error_code: int = None,
        status: int = None,
        url: str = None,
    ):
        self.AlternateUrl = alternate_url
        self.CorrelationId = correlation_id
        self.ErrorCode = error_code
        self.Status = status
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.CollaborationMailboxResponse"
