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

from office365.runtime.schema import TypeSchema
from office365.sharepoint.publishing.pages.page import SitePage

_SITE_PAGE = TypeSchema.of(SitePage)

#: The fields that may carry a page body, modern first.
BODY_FIELDS: Tuple[str, ...] = (_SITE_PAGE.name_of("canvas_content"), _SITE_PAGE.name_of("wiki"))

#: What a page copy projects: identity, both bodies, the layout, and the
#: metadata a Site Pages library keeps as list item properties.
PAGE_FIELDS: Tuple[str, ...] = (
    _SITE_PAGE.name_of("id"),
    _SITE_PAGE.name_of("file_leaf_ref"),
    _SITE_PAGE.name_of("title"),
    _SITE_PAGE.name_of("description"),
    _SITE_PAGE.name_of("content_type_id"),
    _SITE_PAGE.name_of("canvas_content"),
    _SITE_PAGE.name_of("layout_web_parts_content"),
    _SITE_PAGE.name_of("wiki"),
    _SITE_PAGE.name_of("promoted_state"),
    _SITE_PAGE.name_of("banner_image_url"),
    _SITE_PAGE.name_of("moderation_status"),
)
