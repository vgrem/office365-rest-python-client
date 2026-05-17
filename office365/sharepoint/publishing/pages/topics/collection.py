from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.publishing.pages.topics.topic import TopicSitePage


class TopicPageCollection(EntityCollection[TopicSitePage]):
    """Publishing topic site page collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, TopicSitePage, resource_path)
