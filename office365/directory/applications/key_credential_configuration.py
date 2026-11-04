from __future__ import annotations

from dataclasses import field
from datetime import datetime, timedelta

from office365.directory.policies.app_management_policy_actor_exemptions import AppManagementPolicyActorExemptions
from office365.directory.policies.appkeycredentialrestrictiontype import AppKeyCredentialRestrictionType
from office365.directory.policies.appmanagementrestrictionstate import AppManagementRestrictionState
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class KeyCredentialConfiguration(ClientValue):
    excludeActors: AppManagementPolicyActorExemptions = field(default_factory=AppManagementPolicyActorExemptions)
    maxLifetime: timedelta | None = None
    restrictForAppsCreatedAfterDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    restrictionType: AppKeyCredentialRestrictionType = AppKeyCredentialRestrictionType.asymmetricKeyLifetime
    state: AppManagementRestrictionState = AppManagementRestrictionState.enabled

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.KeyCredentialConfiguration"
