from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class HighlightsInfo(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "SP.Publishing.HighlightsInfo"

    @odata(name="HiddenHighlights")
    @property
    def hidden_highlights(self) -> Optional[str]:
        """Gets the HiddenHighlights property"""
        return self.properties.get("HiddenHighlights", None)

    @odata(name="HideListEditor")
    @property
    def hide_list_editor(self) -> Optional[str]:
        """Gets the HideListEditor property"""
        return self.properties.get("HideListEditor", None)
