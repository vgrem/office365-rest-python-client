from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change


class ChangeField(Change):
    """Specifies a change on a field"""

    @odata(name="FieldId")
    @property
    def field_id(self) -> Optional[str]:
        """Identifies the changed field"""
        return self.properties.get("FieldId", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)
