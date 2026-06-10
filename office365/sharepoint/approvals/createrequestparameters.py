from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ApprovalsCreateRequestParameters(ClientValue):
    approvers: Optional[str] = None
    details: Optional[str] = None
    item_id: Optional[str] = None
    item_url_type: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    awaitAll: bool | None = None
    itemId: str | None = None
    itemUrlType: int | None = None
    listId: str | None = None
    markDocAsFinal: bool | None = None
