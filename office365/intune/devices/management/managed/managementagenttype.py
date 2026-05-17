from enum import Enum


class ManagementAgentType(Enum):
    eas = "1"
    mdm = "2"
    easMdm = "3"
    intuneClient = "4"
    easIntuneClient = "5"
    configurationManagerClient = "8"
    configurationManagerClientMdm = "10"
    configurationManagerClientMdmEas = "11"
    unknown = "16"
    jamf = "32"
    googleCloudDevicePolicyController = "64"
    microsoft365ManagedMdm = "258"
    msSense = "1024"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagementAgentType"
