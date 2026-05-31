from __future__ import annotations

from dataclasses import dataclass, field

from office365.onenote.pages.preview_links import OnenotePagePreviewLinks
from office365.runtime.client_value import ClientValue


@dataclass
class OnenotePagePreview(ClientValue):
    links: OnenotePagePreviewLinks = field(default_factory=OnenotePagePreviewLinks)
    previewText: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenotePagePreview"
