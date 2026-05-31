from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Album(ClientValue):
    """
    A photo album is a way to virtually group driveItems with photo facets together in a bundle.
    Bundles of this type will have the album property set on the bundle resource.
    """

    coverImageItemId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Album"
