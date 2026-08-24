from __future__ import annotations

from office365.runtime.client_object import ClientObject
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath


class TaxonomyItem(ClientObject):
    """The TaxonomyItem class is a base class that represents an item in the TermStore (section 3.1.5.23).
    A TaxonomyItem has a name and a unique identifier. It also contains date and time of when the item is created and
    when the item is last modified."""

    def __str__(self) -> str:
        return self.name or self.entity_type_name

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r})"

    @property
    def id(self) -> str | None:
        """Gets the Id of the current TaxonomyItem"""
        return self.properties.get("id", None)

    @property
    def name(self) -> str | None:
        """Gets the name of the current TaxonomyItem object"""
        return self.properties.get("name", None)

    @property
    def property_ref_name(self) -> str:
        return "id"

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        if name == self.property_ref_name:
            if self._resource_path is None:
                if self.parent_collection is None:
                    self._resource_path = ResourcePath(value)
                elif isinstance(self.parent_collection.resource_path, EntityPath):
                    self._resource_path = EntityPath(value, self.parent_collection.resource_path.collection)
                else:
                    self._resource_path = ResourcePath(value, self.parent_collection.resource_path)
            else:
                self._resource_path.set_segment(value)
        return self
