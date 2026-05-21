from dataclasses import dataclass, field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


@dataclass
class OnenotePagePreviewLinks(ClientValue):
    """"""

    previewImageUrl: ExternalLink = field(default_factory=ExternalLink)
