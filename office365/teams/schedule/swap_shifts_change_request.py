from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SwapShiftsChangeRequest(Entity):
    @odata(name="recipientShiftId")
    @property
    def recipient_shift_id(self) -> Optional[str]:
        """Gets the recipientShiftId property"""
        return self.properties.get("recipientShiftId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SwapShiftsChangeRequest"
