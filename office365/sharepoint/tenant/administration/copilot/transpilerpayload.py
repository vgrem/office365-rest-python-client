from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.copilot.transpilerstatement import (
    TranspilerStatement,
)


class CopilotTranspilerPayload(ClientValue):

    def __init__(
        self,
        statement_list: ClientValueCollection[TranspilerStatement] = ClientValueCollection(TranspilerStatement),
    ):
        self.StatementList = statement_list

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.CopilotTranspilerPayload"
