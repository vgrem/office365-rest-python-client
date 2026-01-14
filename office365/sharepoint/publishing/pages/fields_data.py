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


class SitePageFieldsData(ClientValue):
    def __init__(
        self,
        title=None,
        banner_image_url=None,
        canvas_content=None,
        topic_header=None,
        publish_start_date=None,
        author_byline: StringCollection = StringCollection(),
        authoring_metadata: SitePageAuthoringMetadata = SitePageAuthoringMetadata(),
        boost_properties: SitePageBoostProperties = SitePageBoostProperties(),
        call_to_action: str = None,
        canvas_content1: str = None,
        canvas_json1: str = None,
        categories: str = None,
        co_auth_state: SitePageCoAuthState = SitePageCoAuthState(),
        collaborators: ClientValueCollection[SitePageCollaborator] = ClientValueCollection(SitePageCollaborator),
        description: str = None,
        email_transpile_content: str = None,
        hidden_highlights_metadata: str = None,
        hide_list_editor_metadata: str = None,
        layout_webparts_content: str = None,
        modified: datetime = None,
        teams_transpile_content: str = None,
        web_transpile_content: str = None,
    ):
        """
        Represents Site Page metadata for use in page authoring operations.

        :param str title: the Page title
        :param str banner_image_url: the preview image Url for the current Site Page.
        :param str canvas_content: CanvasContent1 for the current Site Page.
        :param str topic_header: TopicHeader of the current Site Page
        :param datetime.datetime publish_start_date:
        """
        super().__init__()
        self.BannerImageUrl = banner_image_url
        self.CanvasContent1 = canvas_content
        self.CanvasJson1 = None
        self.Title = title
        self.TopicHeader = topic_header
        self.PublishStartDate = None
        if publish_start_date is not None:
            self.PublishStartDate = publish_start_date.isoformat()
        self.AuthorByline = author_byline
        self.AuthoringMetadata = authoring_metadata
        self.BoostProperties = boost_properties
        self.CallToAction = call_to_action
        self.CanvasContent1 = canvas_content1
        self.CanvasJson1 = canvas_json1
        self.Categories = categories
        self.CoAuthState = co_auth_state
        self.Collaborators = collaborators
        self.Description = description
        self.EmailTranspileContent = email_transpile_content
        self.HiddenHighlightsMetadata = hidden_highlights_metadata
        self.HideListEditorMetadata = hide_list_editor_metadata
        self.LayoutWebpartsContent = layout_webparts_content
        self.Modified = modified
        self.TeamsTranspileContent = teams_transpile_content
        self.WebTranspileContent = web_transpile_content

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageFieldsData"
