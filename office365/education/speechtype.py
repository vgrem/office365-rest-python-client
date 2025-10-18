from enum import Enum


class EducationSpeechType(Enum):
    informative = "0"
    personal = "1"
    persuasive = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationSpeechType"
