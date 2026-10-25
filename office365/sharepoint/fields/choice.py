from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.fields.multi_choice import FieldMultiChoice


class FieldChoice(FieldMultiChoice):
    """Represents a choice field control."""

    @odata(name="EditFormat")
    @property
    def edit_format(self) -> Optional[int]:
        """Gets the EditFormat property"""
        return self.properties.get("EditFormat", None)
