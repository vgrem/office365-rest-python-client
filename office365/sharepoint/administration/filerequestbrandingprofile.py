from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class FileRequestBrandingProfile(ClientValue):
    BackgroundFileId: Optional[UUID] = None
    BackgroundFileName: Optional[str] = None
    BackgroundFileUrl: Optional[str] = None
    LogoFileId: Optional[UUID] = None
    LogoFileName: Optional[str] = None
    LogoFileUrl: Optional[str] = None
    ProfileType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingProfile"
