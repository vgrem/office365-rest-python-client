from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class AutoLabellingWorkInformation(ClientValue):
    RoutingHint: str | None = None
    ScaleUnitId: UUID | None = None
    Watermark: str | None = None
    WorkItemType: int | None = None
