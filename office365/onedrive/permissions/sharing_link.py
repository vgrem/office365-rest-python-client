from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity import Identity
from office365.runtime.client_value import ClientValue


@dataclass
class SharingLink(ClientValue):
    """The SharingLink resource groups link-related data items into a single structure."""

    type: str | None = None
    scope: str | None = None
    webHtml: str | None = None
    webUrl: str | None = None
    preventsDownload: bool | None = None
    application: Identity | None = field(default_factory=Identity)

    def __repr__(self):
        return self.webUrl or ""
