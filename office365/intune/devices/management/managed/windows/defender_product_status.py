from __future__ import annotations

from enum import Enum


class WindowsDefenderProductStatus(Enum):
    noStatus = "0"
    serviceNotRunning = "1"
    serviceStartedWithoutMalwareProtection = "2"
    pendingFullScanDueToThreatAction = "4"
    pendingRebootDueToThreatAction = "8"
    pendingManualStepsDueToThreatAction = "16"
    avSignaturesOutOfDate = "32"
    asSignaturesOutOfDate = "64"
    noQuickScanHappenedForSpecifiedPeriod = "128"
    noFullScanHappenedForSpecifiedPeriod = "256"
    systemInitiatedScanInProgress = "512"
    systemInitiatedCleanInProgress = "1024"
    samplesPendingSubmission = "2048"
    productRunningInEvaluationMode = "4096"
    productRunningInNonGenuineMode = "8192"
    productExpired = "16384"
    offlineScanRequired = "32768"
    serviceShutdownAsPartOfSystemShutdown = "65536"
    threatRemediationFailedCritically = "131072"
    threatRemediationFailedNonCritically = "262144"
    noStatusFlagsSet = "524288"
    platformOutOfDate = "1048576"
    platformUpdateInProgress = "2097152"
    platformAboutToBeOutdated = "4194304"
    signatureOrPlatformEndOfLifeIsPastOrIsImpending = "8388608"
    windowsSModeSignaturesInUseOnNonWin10SInstall = "16777216"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderProductStatus"
