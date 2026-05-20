from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ApprovalsCreateRequestParameters(ClientValue):
    approvers: Optional[str] = None
    await_all: Optional[bool] = None
    details: Optional[str] = None
    item_id: Optional[str] = None
    item_url_type: Optional[int] = None
    list_id: Optional[str] = None
    mark_doc_as_final: Optional[bool] = None
    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
