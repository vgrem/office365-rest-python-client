from typing import Optional

from office365.runtime.client_value import ClientValue


class SemanticSearchCrawlerEnqueueItem(ClientValue):
    def __init__(
        self,
        associate_site_id: Optional[str] = None,
        item_unique_id: Optional[str] = None,
        seconds_in_db: Optional[int] = None,
        semantic_search_service_end_point_json: Optional[str] = None,
        source_action: Optional[int] = None,
        work_item_id: Optional[str] = None,
        item_id: Optional[int] = None,
        item_url: Optional[str] = None,
        list_id: Optional[str] = None,
        vroom_id: Optional[str] = None,
    ):
        self.associate_site_id = associate_site_id
        self.item_unique_id = item_unique_id
        self.seconds_in_db = seconds_in_db
        self.semantic_search_service_end_point_json = semantic_search_service_end_point_json
        self.source_action = source_action
        self.work_item_id = work_item_id
        self.ItemId = item_id
        self.ItemUrl = item_url
        self.ListId = list_id
        self.VroomId = vroom_id
