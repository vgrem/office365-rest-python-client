from office365.runtime.client_value import ClientValue
from typing import Optional


class TranspilerStatement(ClientValue):
    def __init__(
        self, arguments: Optional[dict] = None, returns: Optional[str] = None, statement_name: Optional[str] = None
    ):
        self.Arguments = arguments
        self.Returns = returns
        self.StatementName = statement_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.TranspilerStatement"
