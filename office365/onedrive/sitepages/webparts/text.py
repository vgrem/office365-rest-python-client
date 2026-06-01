from typing import Optional

from office365.onedrive.sitepages.webparts.web_part import WebPart


class TextWebPart(WebPart):
    """Represents a text web part instance on a SharePoint page."""

    @property
    def inner_html(self) -> Optional[str]:
        """Gets the innerHtml property"""
        return self.properties.get("innerHtml", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TextWebPart"
