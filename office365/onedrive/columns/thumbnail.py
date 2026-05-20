from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ThumbnailColumn(ClientValue):
    """This column stores thumbnail values."""

    isPicture: bool | None = None
