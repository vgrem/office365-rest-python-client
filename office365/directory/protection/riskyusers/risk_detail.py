from enum import Enum


class RiskDetail(Enum):
    """ """

    none = "0"
    adminGeneratedTemporaryPassword = "1"
    userPerformedSecuredPasswordChange = "2"
    userPerformedSecuredPasswordReset = "3"
    adminConfirmedSigninSafe = "4"
    aiConfirmedSigninSafe = "5"
    userPassedMFADrivenByRiskBasedPolicy = "6"
    adminDismissedAllRiskForUser = "7"
    adminConfirmedSigninCompromised = "8"
    hidden = "9"
    adminConfirmedUserCompromised = "10"
    unknownFutureValue = "11"
    adminConfirmedServicePrincipalCompromised = "13"
    adminDismissedAllRiskForServicePrincipal = "14"
    m365DAdminDismissedDetection = "12"
    userChangedPasswordOnPremises = "15"
    adminDismissedRiskForSignIn = "16"
    adminConfirmedAccountSafe = "17"

    @property
    def entity_type_name(self):
        return "microsoft.graph.riskDetail"
