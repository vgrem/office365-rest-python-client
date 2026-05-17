from typing import Optional

from office365.sharepoint.entity import Entity


class ModernizeHomepageResult(Entity):
    """"""

    @property
    def can_modernize_homepage(self) -> Optional[bool]:
        """"""
        return self.properties.get("CanModernizeHomepage", None)
