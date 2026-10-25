from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ModernizeHomepageResult(Entity):
    """"""

    @odata(name="CanModernizeHomepage")
    @property
    def can_modernize_homepage(self) -> Optional[bool]:
        """"""
        return self.properties.get("CanModernizeHomepage", None)

    @odata(name="Reason")
    @property
    def reason(self) -> Optional[str]:
        """Gets the Reason property"""
        return self.properties.get("Reason", None)
