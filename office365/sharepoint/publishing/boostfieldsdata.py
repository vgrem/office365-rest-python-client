from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class BoostFieldsData(ClientValue):
    def __init__(
        self,
        boost_order_type: Optional[int] = None,
        boost_until_seen: Optional[bool] = None,
        expiry: Optional[datetime] = None,
        impressions: Optional[int] = None,
        next_item_id: Optional[int] = None,
        next_item_version: Optional[int] = None,
        previous_item_id: Optional[int] = None,
        previous_item_version: Optional[int] = None,
    ):
        self.BoostOrderType = boost_order_type
        self.BoostUntilSeen = boost_until_seen
        self.Expiry = expiry
        self.Impressions = impressions
        self.NextItemId = next_item_id
        self.NextItemVersion = next_item_version
        self.PreviousItemId = previous_item_id
        self.PreviousItemVersion = previous_item_version

    @property
    def entity_type_name(self):
        return "SP.Publishing.BoostFieldsData"
