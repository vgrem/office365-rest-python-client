from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Thumbnail(ClientValue):
    """
    The thumbnail resource type represents a thumbnail for an image, video, document,
        or any item that has a bitmap representation.
    """

    content: str | None = None
    height: int | None = None
    sourceItemId: str | None = None
    url: str | None = None
    width: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Thumbnail"
