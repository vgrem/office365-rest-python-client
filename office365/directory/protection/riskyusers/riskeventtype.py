from enum import Enum


class RiskEventType(Enum):
    unlikelyTravel = "0"
    anonymizedIPAddress = "1"
    maliciousIPAddress = "2"
    unfamiliarFeatures = "3"
    malwareInfectedIPAddress = "4"
    suspiciousIPAddress = "5"
    leakedCredentials = "6"
    investigationsThreatIntelligence = "7"
    generic = "8"
    adminConfirmedUserCompromised = "9"
    mcasImpossibleTravel = "10"
    mcasSuspiciousInboxManipulationRules = "11"
    investigationsThreatIntelligenceSigninLinked = "12"
    maliciousIPAddressValidCredentialsBlockedIP = "13"
    unknownFutureValue = "14"

    @property
    def entity_type_name(self):
        return "microsoft.graph.riskEventType"
