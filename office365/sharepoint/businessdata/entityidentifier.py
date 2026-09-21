from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class EntityIdentifier(Entity):
    @property
    def identifier_type(self) -> Optional[str]:
        """Gets the IdentifierType property"""
        return self.properties.get("IdentifierType", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.EntityIdentifier"

    def contains_localized_display_name(self) -> ClientResult[bool]:
        """ContainsLocalizedDisplayName operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "ContainsLocalizedDisplayName", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_default_display_name(self) -> ClientResult[str]:
        """GetDefaultDisplayName operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetDefaultDisplayName", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_localized_display_name(self) -> ClientResult[str]:
        """GetLocalizedDisplayName operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetLocalizedDisplayName", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
