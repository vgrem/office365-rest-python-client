from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ThumbnailColumn(ClientValue):
    """This column stores thumbnail values."""

    isPicture: bool | None = None
