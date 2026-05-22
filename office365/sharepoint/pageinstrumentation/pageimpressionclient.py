from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PageImpressionClient(ClientValue):
    BasePageCorrelationId: Optional[str] = None
    ClientIdToClickInfoMap: Optional[dict] = None

    @property
    def entity_type_name(self):
        return "SP.PageInstrumentation.PageImpressionClient"
