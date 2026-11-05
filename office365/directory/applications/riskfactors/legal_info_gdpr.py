from __future__ import annotations

from office365.directory.applications.data_protection import DataProtection
from office365.directory.applications.user_ownership import UserOwnership
from office365.runtime.client_value import ClientValue


class ApplicationRiskFactorLegalInfoGdpr(ClientValue):
    dataProtection: DataProtection = DataProtection.none
    hasRightToErasure: bool | None = None
    isReportingDataBreaches: bool | None = None
    statementUrl: str | None = None
    userOwnership: UserOwnership = UserOwnership.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorLegalInfoGdpr"
