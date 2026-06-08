from typing import Self, Union

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath


class MePath(EntityPath):
    """SignedIn user resource path"""

    def __init__(self):
        super().__init__("me", None, ResourcePath("users"))

    def set_segment(self, segment: Union[int, str]) -> Self:
        super(MePath, self).set_segment(segment)
        return self
