from office365.runtime.client_value import ClientValue


class TranspilerStatement(ClientValue):

    def __init__(
        self, arguments: dict = None, returns: str = None, statement_name: str = None
    ):
        self.Arguments = arguments
        self.Returns = returns
        self.StatementName = statement_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.TranspilerStatement"
