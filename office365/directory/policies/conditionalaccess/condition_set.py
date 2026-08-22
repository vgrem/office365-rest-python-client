from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.applications import ConditionalAccessApplications
from office365.directory.policies.conditionalaccess.authentication_flows import ConditionalAccessAuthenticationFlows
from office365.directory.policies.conditionalaccess.client_applications import ConditionalAccessClientApplications
from office365.directory.policies.conditionalaccess.clientapp import ConditionalAccessClientApp
from office365.directory.policies.conditionalaccess.devices import ConditionalAccessDevices
from office365.directory.policies.conditionalaccess.insiderrisklevels import ConditionalAccessInsiderRiskLevels
from office365.directory.policies.conditionalaccess.locations import ConditionalAccessLocations
from office365.directory.policies.conditionalaccess.platforms import ConditionalAccessPlatforms
from office365.directory.policies.conditionalaccess.users import ConditionalAccessUsers
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ConditionalAccessConditionSet(ClientValue):
    insiderRiskLevels: ConditionalAccessInsiderRiskLevels = ConditionalAccessInsiderRiskLevels.minor
    servicePrincipalRiskLevels: ClientValueCollection[RiskLevel] = field(
        default_factory=lambda: ClientValueCollection(RiskLevel)
    )
    signInRiskLevels: ClientValueCollection[RiskLevel] = field(default_factory=lambda: ClientValueCollection(RiskLevel))
    userRiskLevels: ClientValueCollection[RiskLevel] = field(default_factory=lambda: ClientValueCollection(RiskLevel))
    applications: ConditionalAccessApplications = field(default_factory=ConditionalAccessApplications)
    authenticationFlows: ConditionalAccessAuthenticationFlows = field(
        default_factory=ConditionalAccessAuthenticationFlows
    )
    clientApplications: ConditionalAccessClientApplications = field(default_factory=ConditionalAccessClientApplications)
    clientAppTypes: ClientValueCollection[ConditionalAccessClientApp] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessClientApp)
    )
    devices: ConditionalAccessDevices = field(default_factory=ConditionalAccessDevices)
    locations: ConditionalAccessLocations = field(default_factory=ConditionalAccessLocations)
    platforms: ConditionalAccessPlatforms = field(default_factory=ConditionalAccessPlatforms)
    users: ConditionalAccessUsers = field(default_factory=ConditionalAccessUsers)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessConditionSet"
