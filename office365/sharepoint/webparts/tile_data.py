from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class TileData(ClientValue):
    """Represents a Tile that describes a graphical link the user can click."""

    def __init__(
        self,
        background_collage_image_locations=None,
        background_image_location=None,
        background_image_renders_as_icon=None,
        body_text=None,
        description=None,
        hover_disabled=None,
        id_=None,
        is_wide: Optional[bool] = None,
        link_location: Optional[str] = None,
        tile_order: Optional[int] = None,
        title: Optional[str] = None,
        transparent_overlay: Optional[bool] = None,
    ):
        self.BackgroundCollageImageLocations = StringCollection(background_collage_image_locations)
        self.BackgroundImageLocation = background_image_location
        self.BackgroundImageRendersAsIcon = background_image_renders_as_icon
        self.BodyText = body_text
        self.Description = description
        self.HoverDisabled = hover_disabled
        self.ID = id_
        self.IsWide = is_wide
        self.LinkLocation = link_location
        self.TileOrder = tile_order
        self.Title = title
        self.TransparentOverlay = transparent_overlay

    @property
    def entity_type_name(self):
        return "SP.WebParts.TileData"
