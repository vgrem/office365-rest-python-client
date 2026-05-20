from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SemanticSearchCrawlerEnqueueItem(ClientValue):
    associate_site_id: str | None = None
    item_unique_id: str | None = None
    seconds_in_db: int | None = None
    semantic_search_service_end_point_json: str | None = None
    source_action: int | None = None
    work_item_id: str | None = None
    ItemId: int | None = None
    ItemUrl: str | None = None
    ListId: str | None = None
    VroomId: str | None = None
