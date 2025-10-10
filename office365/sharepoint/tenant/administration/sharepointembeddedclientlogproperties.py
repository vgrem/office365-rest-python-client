from office365.runtime.client_value import ClientValue


class SharePointEmbeddedClientLogProperties(ClientValue):

    def __init__(
        self,
        identifier: str = None,
        log_message: str = None,
        log_type: int = None,
        operation: int = None,
        operation_status: int = None,
    ):
        self.Identifier = identifier
        self.LogMessage = log_message
        self.LogType = log_type
        self.Operation = operation
        self.OperationStatus = operation_status

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SharePointEmbeddedClientLogProperties"
