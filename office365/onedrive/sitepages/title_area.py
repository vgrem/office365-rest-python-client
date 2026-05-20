from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TitleArea(ClientValue):
    """Represents the title area of a given SharePoint page."""

    alternativeText: str | None = None
    enableGradientEffect: bool | None = None
    imageWebUrl: str | None = None
    showAuthor: bool | None = None
