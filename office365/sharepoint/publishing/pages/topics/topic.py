from typing import Optional

from office365.sharepoint.publishing.pages.page import SitePage


class TopicSitePage(SitePage):

    @property
    def entity_id(self):
        return self.properties.get("EntityId", None)

    @property
    def entity_type(self):
        return self.properties.get("EntityType", None)

    @property
    def entity_relations(self) -> Optional[str]:
        """Gets the EntityRelations property"""
        return self.properties.get("EntityRelations", None)

    @property
    def verified_topic_allowed_editors(self) -> Optional[str]:
        """Gets the VerifiedTopicAllowedEditors property"""
        return self.properties.get("VerifiedTopicAllowedEditors", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.TopicSitePage"
