from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CustomizedFormsPage(ClientValue):
    formType: Optional[str] = None
    pageId: Optional[str] = None
    Url: Optional[str] = None
    webpartId: Optional[str] = None
