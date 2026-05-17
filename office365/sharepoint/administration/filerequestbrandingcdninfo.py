from office365.runtime.client_value import ClientValue
from typing import Optional


class FileRequestBrandingCdnInfo(ClientValue):
    def __init__(
        self, background_file_public_cdn_url: Optional[str] = None, logo_file_public_cdn_url: Optional[str] = None
    ):
        self.BackgroundFilePublicCdnUrl = background_file_public_cdn_url
        self.LogoFilePublicCdnUrl = logo_file_public_cdn_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingCdnInfo"
