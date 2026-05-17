from enum import Enum


class TeamSpecialization(Enum):
    none = "0"
    educationStandard = "1"
    educationClass = "2"
    educationProfessionalLearningCommunity = "3"
    educationStaff = "4"
    healthcareStandard = "5"
    healthcareCareCoordination = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamSpecialization"
