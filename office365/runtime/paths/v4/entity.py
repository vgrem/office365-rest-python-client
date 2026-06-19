from __future__ import annotations

from typing import Union

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath


class EntityPath(ResourcePath):
    def __init__(
        self, segment: str | None = None, parent: ResourcePath | None = None, collection: ResourcePath | None = None
    ) -> None:
        super().__init__(segment, parent)
        self._collection = collection

    @property
    def collection(self):
        return self._collection

    @property
    def segment(self):
        return str(self._key or "<key>")

    def set_segment(self, segment: Union[int, str]) -> Self:
        """Patches the path"""
        self._key = segment
        from office365.onedrive.internal.paths.children import ChildrenPath
        from office365.teams.internal.paths.joined_teams import JoinedTeamsPath

        if self._collection is not None:
            self._parent = self._collection
        elif isinstance(self.parent, ChildrenPath):
            self._parent = self.parent.collection
        elif isinstance(self.parent, JoinedTeamsPath):
            self._parent = self.parent.collection
        else:
            self._parent = self.parent
        return self
