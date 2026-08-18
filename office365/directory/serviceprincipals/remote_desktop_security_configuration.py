from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class RemoteDesktopSecurityConfiguration(Entity):
    @property
    def is_remote_desktop_protocol_enabled(self) -> Optional[bool]:
        """Gets the isRemoteDesktopProtocolEnabled property"""
        return self.properties.get("isRemoteDesktopProtocolEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemoteDesktopSecurityConfiguration"
