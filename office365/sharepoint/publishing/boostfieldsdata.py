from datetime import datetime

from office365.runtime.client_value import ClientValue


class BoostFieldsData(ClientValue):

    def __init__(
        self,
        boost_order_type: int = None,
        boost_until_seen: bool = None,
        expiry: datetime = None,
        impressions: int = None,
        next_item_id: int = None,
        next_item_version: int = None,
        previous_item_id: int = None,
        previous_item_version: int = None,
    ):
        self.BoostOrderType = boost_order_type
        self.BoostUntilSeen = boost_until_seen
        self.Expiry = expiry
        self.Impressions = impressions
        self.NextItemId = next_item_id
        self.NextItemVersion = next_item_version
        self.PreviousItemId = previous_item_id
        self.PreviousItemVersion = previous_item_version
