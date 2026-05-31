from __future__ import annotations

from dataclasses import dataclass, field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


@dataclass
class SectionLinks(ClientValue):
    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SectionLinks"
