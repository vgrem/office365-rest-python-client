from enum import Enum


class LifecycleEventType(Enum):
    missed = "0"
    subscriptionRemoved = "1"
    reauthorizationRequired = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LifecycleEventType"
