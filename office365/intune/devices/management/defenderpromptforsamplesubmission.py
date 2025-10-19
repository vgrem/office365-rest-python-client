from enum import Enum


class DefenderPromptForSampleSubmission(Enum):
    userDefined = "0"
    alwaysPrompt = "1"
    promptBeforeSendingPersonalData = "2"
    neverSendData = "3"
    sendAllDataWithoutPrompting = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DefenderPromptForSampleSubmission"
