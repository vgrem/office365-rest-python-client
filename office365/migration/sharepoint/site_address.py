"""An address to name a web by, when a note or a report has to point at one.

:attr:`~office365.sharepoint.webs.web.Web.absolute_url` answers ``None`` when a read
dropped both spellings of a web's URL, and deliberately: a web does not infer its
location from the context it was reached through, which may be bound to another site.
A report cannot take that position -- a note about a web with no address names nothing
-- and the run did reach a site, so that site's base URL is the address an operator can
act on.

One expression, because five modules ask the question: branding, web settings, site
verification, navigation rewriting and the resolver's failure messages all write a note
that has to say *which* web it is about.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from office365.sharepoint.webs.web import Web

__all__ = ["web_url"]


def web_url(web: "Web") -> str:
    """The web's own URL, or the base URL of the site its context is bound to."""
    return web.absolute_url or str(web.context.base_url or "")
