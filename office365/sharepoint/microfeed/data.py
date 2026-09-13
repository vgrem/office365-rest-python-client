from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class MicrofeedData(Entity):
    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedData"

    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @property
    def data(self) -> Optional[dict]:
        """Gets the Data property"""
        return self.properties.get("Data", dict())

    @property
    def definition_id(self) -> Optional[int]:
        """Gets the DefinitionId property"""
        return self.properties.get("DefinitionId", None)

    @property
    def item_type(self) -> Optional[int]:
        """Gets the ItemType property"""
        return self.properties.get("ItemType", None)

    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

    @property
    def target_identifier(self) -> Optional[str]:
        """Gets the TargetIdentifier property"""
        return self.properties.get("TargetIdentifier", None)

    @property
    def version(self) -> Optional[str]:
        """Gets the Version property"""
        return self.properties.get("Version", None)

    def delete_all(self) -> Self:
        """DeleteAll operation."""
        qry = ServiceOperationQuery(self, "DeleteAll", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def add_attachment(self, name: str, bytes_: bytes) -> Self:
        """AddAttachment operation.

        Args:
            name (str): name parameter
            bytes_ (bytes): bytes parameter
        """
        qry = ServiceOperationQuery(self, "AddAttachment", None, {"name": name, "bytes": bytes_}, None, None)
        self.context.add_query(qry)
        return self

    def system_update(self) -> Self:
        """SystemUpdate operation."""
        qry = ServiceOperationQuery(self, "SystemUpdate", None, {}, None, None)
        self.context.add_query(qry)
        return self
