from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.publishing.pages.boostproperties import (
    SitePageBoostProperties,
)
from office365.sharepoint.publishing.pages.coauth_state import SitePageCoAuthState
from office365.sharepoint.publishing.pages.collaborator import SitePageCollaborator
from office365.sharepoint.publishing.sitepageauthoringmetadata import (
    SitePageAuthoringMetadata,
)


@dataclass
class SitePageFieldsData(ClientValue):
    """Represents Site Page metadata for use in page authoring operations.

    Args:
        title (str): the Page title
        banner_image_url (str): the preview image Url for the current Site Page.
        canvas_content1 (str): CanvasContent1 for the current Site Page.
        topic_header (str): TopicHeader of the current Site Page
        publish_start_date (datetime.datetime):
    """

    Title: str | None = None
    BannerImageUrl: str | None = None
    TopicHeader: str | None = None
    PublishStartDate: str | None = None
    AuthorByline: StringCollection = field(default_factory=StringCollection)
    AuthoringMetadata: SitePageAuthoringMetadata = field(default_factory=SitePageAuthoringMetadata)
    BoostProperties: SitePageBoostProperties = field(default_factory=SitePageBoostProperties)
    CallToAction: str | None = None
    CanvasContent1: str | None = None
    CanvasJson1: str | None = None
    Categories: str | None = None
    CoAuthState: SitePageCoAuthState = field(default_factory=SitePageCoAuthState)
    Collaborators: ClientValueCollection[SitePageCollaborator] = field(
        default_factory=lambda: ClientValueCollection(SitePageCollaborator)
    )
    Description: str | None = None
    EmailTranspileContent: str | None = None
    HiddenHighlightsMetadata: str | None = None
    HideListEditorMetadata: str | None = None
    LayoutWebpartsContent: str | None = None
    Modified: datetime | None = None
    TeamsTranspileContent: str | None = None
    WebTranspileContent: str | None = None

    def __post_init__(self):
        if isinstance(self.PublishStartDate, datetime):
            self.PublishStartDate = self.PublishStartDate.isoformat()

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageFieldsData"
