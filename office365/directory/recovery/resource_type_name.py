from __future__ import annotations

from enum import Enum


class ResourceTypeName(Enum):
    user = "0"
    group = "1"
    conditionalAccessPolicy = "2"
    namedLocationPolicy = "3"
    authenticationMethodPolicy = "4"
    authorizationPolicy = "5"
    authenticationStrengthPolicy = "6"
    application = "7"
    servicePrincipal = "8"
    unknownFutureValue = "9"
    oAuth2PermissionGrant = "10"
    appRoleAssignment = "11"
    organization = "12"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.ResourceTypeName"
