"""Built-in SharePoint content type IDs — the single source of truth.

A content type ID is hierarchical: a derived content type's ID starts with its
parent's ([MS-WSSCAML] section 2.3.1.4,
https://learn.microsoft.com/en-us/openspecs/sharepoint_protocols/ms-wsscaml/54d27850-497d-454e-bfe5-41c957a5692a).
That is why the modern page family is recognised by a prefix rather than by
equality, and why one row here answers for every page content type derived from
it.

The metadata this client is generated from carries no content type IDs at all, so
each value is read back from a site's own catalog
(``web.available_content_types``), not from the CSDL.
"""

from __future__ import annotations


class SPBuiltInContentTypeId:
    """IDs of the built-in SharePoint content types, spelled as ``StringId`` spells them."""

    #: "Site Page" on a Site Pages library; the parent of every modern page type.
    #: Verified live: the site's own catalog reports exactly this ``StringId``.
    SitePage = "0x0101009D1CB255DA76424F860D91F20E6C4118"
