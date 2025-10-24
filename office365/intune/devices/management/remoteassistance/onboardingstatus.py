from enum import Enum


class RemoteAssistanceOnboardingStatus(Enum):
    notOnboarded = "0"
    onboarding = "1"
    onboarded = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RemoteAssistanceOnboardingStatus"
