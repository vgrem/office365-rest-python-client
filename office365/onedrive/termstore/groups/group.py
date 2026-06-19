from __future__ import annotations

from typing import Self

from office365.entity import Entity
from office365.onedrive.termstore.sets.collection import SetCollection
from office365.runtime.paths.resource_path import ResourcePath


class Group(Entity):
    """Term Group"""

    def delete_object(self) -> Self:
        def _delete_group():
            super(Group, self).delete_object()

        def _on_sets_loaded(sets: SetCollection):
            if len(sets) == 0:
                _delete_group()
            else:
                for s in sets:
                    s.delete_object()
                self.after_execute(lambda _: _delete_group())

        self.sets.get().after_execute(_on_sets_loaded)
        return self

    def __str__(self) -> str:
        return self.display_name or ""

    @property
    def display_name(self) -> str | None:
        """Name of the group."""
        return self.properties.get("displayName", None)

    @property
    def parent_site_id(self) -> str | None:
        """ID of the parent site of this group."""
        return self.properties.get("parentSiteId", None)

    @property
    def sets(self) -> SetCollection:
        """Collection of all sets available in the term store."""
        return self.properties.get(
            "sets",
            SetCollection(self.context, ResourcePath("sets", self.resource_path), self),
        )

    @property
    def entity_type_name(self) -> str:
        return None  # type: ignore
