from typing import Optional

from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class TopicPageFieldsData(SitePageFieldsData):
    def __init__(
        self,
        entity_id=None,
        entity_relations=None,
        entity_type: Optional[str] = None,
        verified_topic_allowed_editors: Optional[str] = None,
    ):
        super().__init__()
        self.EntityId = entity_id
        self.EntityRelations = entity_relations
        self.EntityType = entity_type
        self.VerifiedTopicAllowedEditors = verified_topic_allowed_editors

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "SP.Publishing.TopicPageFieldsData"
