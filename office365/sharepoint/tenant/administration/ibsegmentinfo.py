from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class IBSegmentInfo(ClientValue):
    DisplayName: str | None = None
    ObjectId: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Portal.IBSegmentInfo"
