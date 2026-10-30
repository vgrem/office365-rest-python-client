from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class LandingPageDetail(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[str]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="isDefaultLangauge")
    @property
    def is_default_langauge(self) -> Optional[bool]:
        """Gets the isDefaultLangauge property"""
        return self.properties.get("isDefaultLangauge", None)

    @odata(name="language")
    @property
    def language(self) -> Optional[str]:
        """Gets the language property"""
        return self.properties.get("language", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LandingPageDetail"
