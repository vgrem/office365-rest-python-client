from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.tenant.administration.copilot.transpilerstatement import (
    TranspilerStatement,
)


@value
class CopilotTranspilerPayload(ClientValue):
    StatementList: ClientValueCollection[TranspilerStatement] = field(
        default_factory=lambda: ClientValueCollection(TranspilerStatement)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.CopilotTranspilerPayload"
