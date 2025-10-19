from enum import Enum


class VirtualAppointmentMessageType(Enum):
    confirmation = "0"
    reschedule = "1"
    cancellation = "2"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VirtualAppointmentMessageType"
