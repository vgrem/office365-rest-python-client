from __future__ import annotations

from office365.runtime.client_value import ClientValue


class HyperlinkOrPictureColumn(ClientValue):
    """Represents a hyperlink or picture column in SharePoint."""

    def __init__(self, is_picture: bool | None = None):
        """
        :param bool is_picture: Specifies whether the display format used for URL columns is an image or a hyperlink.
        """
        self.isPicture = is_picture
