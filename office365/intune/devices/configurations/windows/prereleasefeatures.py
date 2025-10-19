from enum import Enum


class PrereleaseFeatures(Enum):
    userDefined = "0"
    settingsOnly = "1"
    settingsAndExperimentations = "2"
    notAllowed = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrereleaseFeatures"
