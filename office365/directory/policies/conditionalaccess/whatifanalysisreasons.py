from enum import Enum


class WhatIfAnalysisReasons(Enum):
    notSet = "0"
    notEnoughInformation = "1"
    invalidCondition = "2"
    users = "4"
    workloadIdentities = "8"
    application = "16"
    userActions = "32"
    authenticationContext = "64"
    devicePlatform = "128"
    devices = "256"
    clientApps = "512"
    location = "1024"
    signInRisk = "2048"
    emptyPolicy = "4096"
    invalidPolicy = "8192"
    policyNotEnabled = "16384"
    userRisk = "32768"
    time = "65536"
    insiderRisk = "131072"
    authenticationFlow = "262144"
    unknownFutureValue = "524288"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WhatIfAnalysisReasons"
