from __future__ import annotations

import json
from os import PathLike
from typing import Optional

from typing_extensions import Self

from office365.directory.permissions.require_permission import require_permission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.termstore.groups.collection import GroupCollection
from office365.onedrive.termstore.sets.collection import SetCollection
from office365.onedrive.termstore.sets.set import Set
from office365.onedrive.termstore.terms.collection import TermCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection


class Store(Entity):
    """Represents a taxonomy term store."""

    @require_permission(
        delegated=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        application=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        notes="Get all term sets across all groups",
    )
    def get_all_term_sets(self) -> EntityCollection[Set]:
        """Returns a collection containing a flat list of all TermSet objects."""
        return_type = EntityCollection(self.context, Set)

        def _sets_loaded(sets: SetCollection) -> None:
            [return_type.add_child(s) for s in sets]

        def _groups_loaded(groups: GroupCollection) -> None:
            [grp.sets.get().after_execute(_sets_loaded) for grp in groups]

        self.groups.get().after_execute(_groups_loaded)
        return return_type

    def import_from_json(self, path: str | PathLike) -> Self:
        """Import term store hierarchy from a JSON file."""

        with open(path) as f:
            data = json.load(f)

        for group_data in data:
            group = self.groups.get_or_add(group_data["name"])
            for set_data in group_data.get("sets", []):
                term_set = group.sets.get_or_add(set_data["name"])
                self._import_terms(term_set.children, set_data.get("children", []))

        return self

    def _import_terms(self, collection: TermCollection, terms: list[dict]):
        for t in terms:
            node = collection.get_or_add(t["name"])
            self._import_terms(node.children, t.get("children", []))

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
