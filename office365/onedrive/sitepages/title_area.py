from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.server_processed_content import ServerProcessedContent
from office365.onedrive.sitepages.titlearealayouttype import TitleAreaLayoutType
from office365.onedrive.sitepages.titleareatextalignmenttype import TitleAreaTextAlignmentType
from office365.runtime.client_value import ClientValue


@dataclass
class TitleArea(ClientValue):
    """Represents the title area of a given SharePoint page."""

    alternativeText: str | None = None
    enableGradientEffect: bool | None = None
    imageWebUrl: str | None = None
    showAuthor: bool | None = None
    layout: TitleAreaLayoutType = TitleAreaLayoutType.imageAndTitle
    serverProcessedContent: ServerProcessedContent = field(default_factory=ServerProcessedContent)
    showPublishedDate: bool | None = None
    showTextBlockAboveTitle: bool | None = None
    textAboveTitle: str | None = None
    textAlignment: TitleAreaTextAlignmentType = TitleAreaTextAlignmentType.left

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TitleArea"
