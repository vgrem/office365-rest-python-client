from __future__ import annotations

from typing import TYPE_CHECKING

from office365.onedrive.internal.paths.root import RootPath
from office365.runtime.paths.v4.entity import EntityPath

if TYPE_CHECKING:
    from office365.runtime.paths.resource_path import ResourcePath


class UrlPath(EntityPath):
    """Resource path for OneDrive entity path-based addressing"""

    def __init__(self, url: str, parent: ResourcePath | None, collection: ResourcePath | None = None) -> None:
        """
        :param str url: File or Folder server relative url
        :type parent: office365.runtime.paths.resource_path.ResourcePath
        """
        if isinstance(parent, UrlPath):
            url = "/".join([str(parent._key), url])
            collection = parent.collection
            parent = parent.parent
        elif isinstance(parent, RootPath):
            collection = parent.collection
        elif isinstance(parent, EntityPath):
            collection = parent.collection
        super().__init__(url, parent, collection)

    @property
    def segment(self):
        return f":/{self._key}:/"

    def set_segment(self, segment):
        self._key = segment
        self.__class__ = EntityPath  # type: ignore
        self._parent = self.collection
        return self

    @property
    def delimiter(self) -> str:
        return ""
