from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identities.authentication_flow import AuthenticationFlow
from office365.directory.policies.conditionalaccess.clientapp import ConditionalAccessClientApp
from office365.directory.policies.conditionalaccess.device_info import DeviceInfo
from office365.directory.policies.conditionalaccess.deviceplatform import ConditionalAccessDevicePlatform
from office365.directory.policies.insiderrisklevel import InsiderRiskLevel
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.runtime.client_value import ClientValue


@dataclass
class SignInConditions(ClientValue):
    authenticationFlow: AuthenticationFlow = field(default_factory=AuthenticationFlow)
    clientAppType: ConditionalAccessClientApp = ConditionalAccessClientApp.all
    country: str | None = None
    deviceInfo: DeviceInfo = field(default_factory=DeviceInfo)
    devicePlatform: ConditionalAccessDevicePlatform = ConditionalAccessDevicePlatform.android
    insiderRiskLevel: InsiderRiskLevel = InsiderRiskLevel.none
    ipAddress: str | None = None
    servicePrincipalRiskLevel: RiskLevel = RiskLevel.low
    signInRiskLevel: RiskLevel = RiskLevel.low
    userRiskLevel: RiskLevel = RiskLevel.low

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SignInConditions"
