from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeOrder(ClientValue):
    """The contentTypeOrder resource specifies in which order the Content Type will appear in the selection UI."""

    default: bool | None = None
    position: str | None = None
