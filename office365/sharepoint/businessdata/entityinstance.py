from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class EntityInstance(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.BusinessData.Runtime.EntityInstance"

    def create_collection_instance(self, field_dot_notation: str, size: int) -> Self:
        """CreateCollectionInstance operation.

        Args:
            field_dot_notation (str): fieldDotNotation parameter
            size (int): size parameter
        """
        qry = ServiceOperationQuery(
            self, "CreateCollectionInstance", None, {"fieldDotNotation": field_dot_notation, "size": size}, None, None
        )
        self.context.add_query(qry)
        return self

    def create_instance(self, field_instance_dot_notation: str, field_dot_notation: str) -> Self:
        """CreateInstance operation.

        Args:
            field_instance_dot_notation (str): fieldInstanceDotNotation parameter
            field_dot_notation (str): fieldDotNotation parameter
        """
        qry = ServiceOperationQuery(
            self,
            "CreateInstance",
            None,
            {"fieldInstanceDotNotation": field_instance_dot_notation, "fieldDotNotation": field_dot_notation},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def from_xml(self, xml: str) -> Self:
        """FromXml operation.

        Args:
            xml (str): xml parameter
        """
        qry = ServiceOperationQuery(self, "FromXml", None, {"xml": xml}, None, None)
        self.context.add_query(qry)
        return self

    def to_xml(self) -> ClientResult[str]:
        """ToXml operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "ToXml", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
