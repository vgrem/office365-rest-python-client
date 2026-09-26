from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class TypeDescriptor(Entity):
    @property
    def contains_read_only(self) -> Optional[bool]:
        """Gets the ContainsReadOnly property"""
        return self.properties.get("ContainsReadOnly", None)

    @property
    def is_collection(self) -> Optional[bool]:
        """Gets the IsCollection property"""
        return self.properties.get("IsCollection", None)

    @property
    def is_read_only(self) -> Optional[bool]:
        """Gets the IsReadOnly property"""
        return self.properties.get("IsReadOnly", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def type_name(self) -> Optional[str]:
        """Gets the TypeName property"""
        return self.properties.get("TypeName", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.TypeDescriptor"

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

    def is_leaf(self) -> ClientResult[bool]:
        """IsLeaf operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "IsLeaf", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_root(self) -> ClientResult[bool]:
        """IsRoot operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "IsRoot", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
