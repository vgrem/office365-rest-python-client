from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MyRecsQueryInfo(ClientValue):
    def __init__(
        self,
        category: int = None,
        expertise_tags: StringCollection = StringCollection(),
        followed_urls: StringCollection = StringCollection(),
        interest_tags: StringCollection = StringCollection(),
        query_info_exists: bool = None,
        suggested_tags: StringCollection = None,
    ):
        self.Category = category
        self.ExpertiseTags = expertise_tags
        self.FollowedUrls = followed_urls
        self.InterestTags = interest_tags
        self.QueryInfoExists = query_info_exists
        self.SuggestedTags = suggested_tags

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Project.MyRecsQueryInfo"
