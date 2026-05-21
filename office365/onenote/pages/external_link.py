from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ExternalLink(ClientValue):
    """Represents a URL that opens a OneNote page or notebook.

    :param str href: The URL of the link.
    """

    href: str | None = None

    def __repr__(self):
        return self.href or ""
