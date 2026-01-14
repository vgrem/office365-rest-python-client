from typing import Optional

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
