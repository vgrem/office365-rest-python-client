from enum import Enum


class OnlineMeetingProviderType(Enum):
    """Specifies the type of a principal."""

    unknown = 0
    ""
    skypeForBusiness = 1
    ""
    skypeForConsumer = 2
    ""
    teamsForBusiness = 3
    ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnlineMeetingProviderType"
