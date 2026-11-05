from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomFontsResource(ClientValue):
    byteArray: Optional[bytes] = None
    fileName: Optional[str] = None
    fullPath: Optional[str] = None
    MajVer: Optional[int] = None
    type: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.CustomFontsResource"
