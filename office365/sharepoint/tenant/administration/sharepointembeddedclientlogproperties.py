from typing import Optional

from office365.runtime.client_value import ClientValue


class SharePointEmbeddedClientLogProperties(ClientValue):
    def __init__(
        self,
        identifier: Optional[str] = None,
        log_message: Optional[str] = None,
        log_type: Optional[int] = None,
        operation: Optional[int] = None,
        operation_status: Optional[int] = None,
    ):
        self.Identifier = identifier
        self.LogMessage = log_message
        self.LogType = log_type
        self.Operation = operation
        self.OperationStatus = operation_status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SharePointEmbeddedClientLogProperties"
