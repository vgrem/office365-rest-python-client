from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ThumbnailColumn(ClientValue):
    """This column stores thumbnail values."""

    isPicture: bool | None = None
