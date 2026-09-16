from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class MigrationProperties(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationProperties"

    @property
    def count(self) -> Optional[int]:
        """Gets the Count property"""
        return self.properties.get("Count", None)

    def delete(self, key: str) -> Self:
        """Delete operation.

        Args:
            key (str): key parameter
        """
        qry = ServiceOperationQuery(self, "Delete", None, {"key": key}, None, None)
        self.context.add_query(qry)
        return self
