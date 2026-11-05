from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.useractivitytype import UserActivityType


class ActivityMetadata(ClientValue):
    activity: UserActivityType = UserActivityType.uploadText

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ActivityMetadata"
