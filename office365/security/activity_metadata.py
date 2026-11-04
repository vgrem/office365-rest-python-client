from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.useractivitytype import UserActivityType


@value
class ActivityMetadata(ClientValue):
    activity: UserActivityType = UserActivityType.uploadText

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ActivityMetadata"
