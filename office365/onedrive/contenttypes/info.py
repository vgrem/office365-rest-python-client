from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeInfo(ClientValue):
    """
    The contentTypeInfo resource indicates the SharePoint content type of an item.
    """

    id: str | None = None
    name: str | None = None
