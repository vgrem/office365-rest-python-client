from datetime import datetime

from office365.runtime.client_value import ClientValue


class SitePageBoostProperties(ClientValue):

    def __init__(
        self,
        boost_order: float = None,
        boost_order_version: int = None,
        boost_until_expiry_date: datetime = None,
        boost_until_seen: bool = None,
        boost_until_users_viewed_count: int = None,
    ):
        self.BoostOrder = boost_order
        self.BoostOrderVersion = boost_order_version
        self.BoostUntilExpiryDate = boost_until_expiry_date
        self.BoostUntilSeen = boost_until_seen
        self.BoostUntilUsersViewedCount = boost_until_users_viewed_count

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageBoostProperties"
