from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class HostedApp(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.HostedApp"

    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def update_web_part_data(self, web_part_data_as_json: str) -> Self:
        """UpdateWebPartData operation.

        Args:
            web_part_data_as_json (str): webPartDataAsJson parameter
        """
        qry = ServiceOperationQuery(
            self, "UpdateWebPartData", None, {"webPartDataAsJson": web_part_data_as_json}, None, None
        )
        self.context.add_query(qry)
        return self
