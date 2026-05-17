from enum import Enum


class MeetingRequestType(Enum):
    none = "0"
    newMeetingRequest = "1"
    fullUpdate = "65536"
    informationalUpdate = "131072"
    silentUpdate = "262144"
    outdated = "524288"
    principalWantsCopy = "1048576"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MeetingRequestType"
