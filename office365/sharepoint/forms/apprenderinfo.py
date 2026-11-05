from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class AppRenderInfo(ClientValue):
    BackgroundColor: Optional[str] = None
    PrimaryDeviceHeight: Optional[str] = None
    PrimaryDeviceWidth: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Internal.AppRenderInfo"
