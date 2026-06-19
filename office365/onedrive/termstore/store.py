from __future__ import annotations

import json
from os import PathLike
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.onedrive.termstore.groups.collection import GroupCollection
from office365.onedrive.termstore.sets.collection import SetCollection
from office365.onedrive.termstore.store_exporter import StoreExporter
from office365.onedrive.termstore.store_importer import StoreImporter
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection


class Store(Entity):
    """Represents a taxonomy term store."""

    def export_to_json(self) -> ClientResult[list]:
        return StoreExporter(self).export()

    def import_from_json(self, path: str | PathLike) -> Self:
        """Import term store hierarchy from a JSON file."""
        with open(path) as f:
            data = json.load(f)
        StoreImporter(self).import_from_data(data)
        return self

    @property
    def default_language_tag(self) -> Optional[str]:
        """Default language of the term store."""
        return self.properties.get("defaultLanguageTag", None)

    @property
    def language_tags(self) -> StringCollection:
        """List of languages for the term store."""
        return self.properties.get("languageTags", StringCollection())

    @property
    def groups(self) -> GroupCollection:
        """Collection of all groups available in the term store."""
        return self.properties.get("groups", GroupCollection(self.context, ResourcePath("groups", self.resource_path)))

    @property
    def sets(self) -> SetCollection:
        """Collection of all sets available in the term store."""
        return self.properties.get("sets", SetCollection(self.context, ResourcePath("sets", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {"languageTags": self.language_tags}
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.termStore.Store"
