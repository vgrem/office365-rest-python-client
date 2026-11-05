from __future__ import annotations

from dataclasses import field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


class SectionLinks(ClientValue):
    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SectionLinks"
