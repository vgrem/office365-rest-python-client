from office365.runtime.client_value import ClientValue
from typing import Optional


class ErrorFacet(ClientValue):
    def __init__(self, code: Optional[str] = None, message: Optional[str] = None):
        self.Code = code
        self.Message = message

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.ErrorFacet"
