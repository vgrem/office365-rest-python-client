from enum import Enum


class AllowedTargetScope(Enum):
    notSpecified = "0"
    specificDirectoryUsers = "1"
    specificConnectedOrganizationUsers = "2"
    specificDirectoryServicePrincipals = "3"
    allMemberUsers = "4"
    allDirectoryUsers = "5"
    allDirectoryServicePrincipals = "6"
    allConfiguredConnectedOrganizationUsers = "7"
    allExternalUsers = "8"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AllowedTargetScope"
