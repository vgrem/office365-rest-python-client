from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantCdnUrl(ClientValue):
    def __init__(
        self,
        cdn_url: Optional[str] = None,
        expiration_time_utc: Optional[datetime] = None,
        is_cdn_url_available: Optional[bool] = None,
        item_url: Optional[str] = None,
    ):
        self.CdnUrl = cdn_url
        self.ExpirationTimeUtc = expiration_time_utc
        self.IsCdnUrlAvailable = is_cdn_url_available
        self.ItemUrl = item_url

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.TenantCdn.TenantCdnUrl"
