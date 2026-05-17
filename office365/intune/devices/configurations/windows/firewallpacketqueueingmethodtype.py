from enum import Enum


class FirewallPacketQueueingMethodType(Enum):
    deviceDefault = "0"
    disabled = "1"
    queueInbound = "2"
    queueOutbound = "3"
    queueBoth = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FirewallPacketQueueingMethodType"
