"""The wire fields a *page item* carries, spelled once.

A page is read through the list-item projection of its library, not through the
``sitepages/pages`` entity: the entity serves only pages whose content type
derives from "Site Page" — a classic wiki page is refused with "This page does
not have the site page content type" — while the item projection answers every
page in the library.

Every name here is derived from :class:`SitePage`, which declares the item columns
too, so a projection cannot drift from the model it reads.
"""

from __future__ import annotations

from typing import Tuple

from office365.sharepoint.publishing.pages.page import SitePage

#: The fields that may carry a page body, modern first.
BODY_FIELDS: Tuple[str, ...] = (SitePage.odata_name("canvas_content"), SitePage.odata_name("wiki"))

#: What a page copy projects: identity, both bodies, the layout, and the
#: metadata a Site Pages library keeps as list item properties.
PAGE_FIELDS: Tuple[str, ...] = (
    SitePage.odata_name("id"),
    SitePage.odata_name("file_leaf_ref"),
    SitePage.odata_name("title"),
    SitePage.odata_name("description"),
    SitePage.odata_name("content_type_id"),
    SitePage.odata_name("canvas_content"),
    SitePage.odata_name("layout_web_parts_content"),
    SitePage.odata_name("wiki"),
    SitePage.odata_name("promoted_state"),
    SitePage.odata_name("banner_image_url"),
    SitePage.odata_name("moderation_status"),
)
