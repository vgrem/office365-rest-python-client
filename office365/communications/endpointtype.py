from enum import Enum


class EndpointType(Enum):
    default = "0"
    voicemail = "1"
    skypeForBusiness = "2"
    skypeForBusinessVoipPhone = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EndpointType"
