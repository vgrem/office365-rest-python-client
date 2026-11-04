from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomizedFormsPage(ClientValue):
    formType: Optional[str] = None
    pageId: Optional[str] = None
    Url: Optional[str] = None
    webpartId: Optional[str] = None
