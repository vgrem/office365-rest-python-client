from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class IRMigration(Entity):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.IR.IRMigration"

    def delete_and_recreate_ir_list(self) -> Self:
        """DeleteAndRecreateIRList operation."""
        qry = ServiceOperationQuery(self, "DeleteAndRecreateIRList", None, {}, None, None)
        self.context.add_query(qry)
        return self
