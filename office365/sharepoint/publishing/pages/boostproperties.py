from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SitePageBoostProperties(ClientValue):
    def __init__(
        self,
        boost_order: Optional[float] = None,
        boost_order_version: Optional[int] = None,
        boost_until_expiry_date: Optional[datetime] = None,
        boost_until_seen: Optional[bool] = None,
        boost_until_users_viewed_count: Optional[int] = None,
    ):
        self.BoostOrder = boost_order
        self.BoostOrderVersion = boost_order_version
        self.BoostUntilExpiryDate = boost_until_expiry_date
        self.BoostUntilSeen = boost_until_seen
        self.BoostUntilUsersViewedCount = boost_until_users_viewed_count

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageBoostProperties"
