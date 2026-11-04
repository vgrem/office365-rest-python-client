from dataclasses import field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class OnenotePagePreviewLinks(ClientValue):
    """"""

    previewImageUrl: ExternalLink = field(default_factory=ExternalLink)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenotePagePreviewLinks"
