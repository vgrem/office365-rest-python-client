from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity_collection import EntityCollection
from office365.onedrive.sitepages.site_page import SitePage
from office365.onedrive.sitepages.title_area import TitleArea
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient
    from office365.onedrive.lists.list import List


class SitePageCollection(EntityCollection[SitePage]):
    """Sites container"""

    def __init__(
        self,
        context: GraphClient,
        resource_path: ResourcePath | None = None,
        parent_list: List | None = None,
    ) -> None:
        super().__init__(context, SitePage, resource_path, parent_list)

    def get_by_name(self, name: str) -> SitePage | None:
        """Get a sitePage by name."""
        return self.single(f"name eq '{name}'")

    def get_by_title(self, title: str) -> SitePage | None:
        """Get a sitePage by title."""
        return self.single(f"title eq '{title}'")

    def add(self, title: str, page_layout: str = "article"):
        """
        Create a new sitePage in the site pages list in a site.

        :param str title:
        :param str page_layout:
        """

        def _construct_request(request: RequestOptions) -> None:
            request.set_header("Content-Type", "application/json")

        return (
            super()
            .add(
                title=title,
                name=f"{title}.aspx",
                pageLayout=page_layout,
                titleArea=TitleArea(),
            )
            .before_execute(_construct_request)
        )
