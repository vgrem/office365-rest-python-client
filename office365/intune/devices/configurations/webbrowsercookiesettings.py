from enum import Enum


class WebBrowserCookieSettings(Enum):
    browserDefault = "0"
    blockAlways = "1"
    allowCurrentWebSite = "2"
    allowFromWebsitesVisited = "3"
    allowAlways = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WebBrowserCookieSettings"
