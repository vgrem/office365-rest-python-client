from __future__ import annotations

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.htmlpages.html_page import HtmlPage


class HtmlPageService(Entity):
    @property
    def pages(self) -> EntityCollection[HtmlPage]:
        """Gets the Pages property"""
        return self.properties.get(
            "Pages", EntityCollection[HtmlPage](self.context, HtmlPage, ResourcePath("Pages", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "SP.HtmlPages.HtmlPageService"
