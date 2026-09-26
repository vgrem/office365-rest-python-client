from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.businessdata.entityfield import EntityField
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection


class EntityView(Entity):
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def related_specific_finder_name(self) -> Optional[str]:
        """Gets the RelatedSpecificFinderName property"""
        return self.properties.get("RelatedSpecificFinderName", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.EntityView"

    @property
    def fields(self) -> EntityCollection[EntityField]:
        """Gets the Fields property"""
        return self.properties.get(
            "Fields",
            EntityCollection[EntityField](self.context, EntityField, ResourcePath("Fields", self.resource_path)),
        )

    def get_type(self, field_dot_notation: str) -> ClientResult[str]:
        """GetType operation.

        Args:
            field_dot_notation (str): fieldDotNotation parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetType", None, {"fieldDotNotation": field_dot_notation}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_xml_schema(self) -> ClientResult[str]:
        """GetXmlSchema operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetXmlSchema", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
