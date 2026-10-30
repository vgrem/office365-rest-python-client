from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.users.user import User
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.teams.administration.account_type import AccountType
from office365.teams.administration.assigned_telephone_number import (
    AssignedTelephoneNumber,
)
from office365.teams.administration.effective_policy_assignment import (
    EffectivePolicyAssignment,
)


class TeamsUserConfiguration(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="effectivePolicyAssignments")
    @property
    def effective_policy_assignments(self) -> ClientValueCollection[EffectivePolicyAssignment]:
        """Gets the effectivePolicyAssignments property"""
        return self.properties.get(
            "effectivePolicyAssignments", ClientValueCollection[EffectivePolicyAssignment](EffectivePolicyAssignment)
        )

    @odata(name="featureTypes")
    @property
    def feature_types(self) -> StringCollection:
        """Gets the featureTypes property"""
        return self.properties.get("featureTypes", StringCollection(None))

    @odata(name="isEnterpriseVoiceEnabled")
    @property
    def is_enterprise_voice_enabled(self) -> Optional[bool]:
        """Gets the isEnterpriseVoiceEnabled property"""
        return self.properties.get("isEnterpriseVoiceEnabled", None)

    @odata(name="modifiedDateTime")
    @property
    def modified_date_time(self) -> Optional[datetime]:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @odata(name="telephoneNumbers")
    @property
    def telephone_numbers(self) -> ClientValueCollection[AssignedTelephoneNumber]:
        """Gets the telephoneNumbers property"""
        return self.properties.get(
            "telephoneNumbers", ClientValueCollection[AssignedTelephoneNumber](AssignedTelephoneNumber)
        )

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @odata(name="user", navigation=True)
    @property
    def user(self) -> User:
        """Gets the user property"""
        return self.properties.get("user", User(self.context, ResourcePath("user", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TeamsUserConfiguration"

    @odata(name="accountType")
    @property
    def account_type(self) -> AccountType:
        """Gets the accountType property"""
        return self.properties.get("accountType", AccountType.user)
