from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.onedrive.termstore.groups.collection import GroupCollection
from office365.onedrive.termstore.groups.group import Group
from office365.onedrive.termstore.sets.collection import SetCollection
from office365.onedrive.termstore.store_manager import StoreManager
from office365.onedrive.termstore.terms.collection import TermCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class Store(Entity):
    """Represents a taxonomy term store."""

    def ensure_group(self, name: str) -> Group:
        """Gets existing group by name or creates a new one (idempotent)."""
        return self.groups.ensure(name)

    def search_term(self, search_label: str) -> TermCollection:
        """Search for a term by label across all sets in the term store."""
        return StoreManager(self).search_term(search_label)

    def get_all_terms(self) -> TermCollection:
        """Flatten the whole term store into a single ``TermCollection`` (deferred)."""
        return StoreManager(self).get_all_terms()

    def from_json(self, data: list[dict]) -> Self:
        """Import a term hierarchy from a list of group dicts (deferred)."""
        StoreManager(self).from_json(data)
        return self

    @property
    def default_language_tag(self) -> Optional[str]:
        """Default language of the term store."""
        return self.properties.get("defaultLanguageTag", None)

    @odata(name="languageTags")
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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.termStore.Store"
