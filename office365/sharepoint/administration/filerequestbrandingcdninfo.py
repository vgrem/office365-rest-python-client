from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class FileRequestBrandingCdnInfo(ClientValue):
    BackgroundFilePublicCdnUrl: Optional[str] = None
    LogoFilePublicCdnUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingCdnInfo"
