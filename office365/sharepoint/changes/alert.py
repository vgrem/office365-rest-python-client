from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change


class ChangeAlert(Change):
    """Specifies a change from an alert."""

    @odata(name="AlertId")
    @property
    def alert_id(self) -> Optional[str]:
        """Identifies the changed alert."""
        return self.properties.get("AlertId", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)
