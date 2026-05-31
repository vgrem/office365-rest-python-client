from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.data_type import ApplicationDataType
from office365.directory.applications.hold_type import HoldType
from office365.directory.applications.location import ApplicationLocation
from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationRiskFactorGeneralInfo(ClientValue):
    consumerPopularity: int | None = None
    founded: int | None = None
    hasDisasterRecoveryPlan: bool | None = None
    hold: HoldType = HoldType.none
    hostingCompanyName: str | None = None
    location: ApplicationLocation = field(default_factory=ApplicationLocation)
    privacyPolicy: str | None = None
    processedDataTypes: ApplicationDataType = ApplicationDataType.none
    termsOfService: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorGeneralInfo"
