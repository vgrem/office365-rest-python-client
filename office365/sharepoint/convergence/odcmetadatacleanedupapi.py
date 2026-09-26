from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class OdcMetadataCleanedUpApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Convergence.OdcMetadataCleanedUpApi"

    def add_state(self) -> Self:
        """AddState operation."""
        qry = ServiceOperationQuery(self, "AddState", None, {}, None, None)
        self.context.add_query(qry)
        return self
