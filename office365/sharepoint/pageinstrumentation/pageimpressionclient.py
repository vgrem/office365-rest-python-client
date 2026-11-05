from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class PageImpressionClient(ClientValue):
    BasePageCorrelationId: Optional[str] = None
    ClientIdToClickInfoMap: Optional[dict] = None

    @property
    def entity_type_name(self):
        return "SP.PageInstrumentation.PageImpressionClient"
