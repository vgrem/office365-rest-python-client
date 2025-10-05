from datetime import datetime

from office365.runtime.client_value import ClientValue


class TenantCdnUrl(ClientValue):

    def __init__(
        self,
        cdn_url: str = None,
        expiration_time_utc: datetime = None,
        is_cdn_url_available: bool = None,
        item_url: str = None,
    ):
        self.CdnUrl = cdn_url
        self.ExpirationTimeUtc = expiration_time_utc
        self.IsCdnUrlAvailable = is_cdn_url_available
        self.ItemUrl = item_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.TenantCdn.TenantCdnUrl"
