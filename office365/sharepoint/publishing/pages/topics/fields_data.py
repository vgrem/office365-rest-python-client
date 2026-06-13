from __future__ import annotations

from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class TopicPageFieldsData(SitePageFieldsData):
    EntityId: str | None = None
    EntityRelations: str | None = None
    EntityType: str | None = None
    VerifiedTopicAllowedEditors: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TopicPageFieldsData"
