from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.directory.authentication.strength.policytype import AuthenticationStrengthPolicyType
from office365.directory.authentication.strength.requirements import AuthenticationStrengthRequirements
from office365.directory.authentication.strength.usage import AuthenticationStrengthUsage
from office365.directory.policies.authentication_combination_configuration import AuthenticationCombinationConfiguration
from office365.directory.policies.update_allowed_combinations_result import UpdateAllowedCombinationsResult
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery


class AuthenticationStrengthPolicy(Entity):
    """
    A collection of settings that define specific combinations of authentication methods and metadata.
    The authentication strength policy, when applied to a given scenario using Azure AD Conditional Access,
    defines which authentication methods must be used to authenticate in that scenario. An authentication strength
    may be built-in or custom (defined by the tenant) and may or may not fulfill the requirements to grant an MFA claim.
    """

    def usage(self) -> ClientResult[AuthenticationStrengthUsage]:
        """
        Allows the caller to see which Conditional Access policies reference a specified authentication strength policy.
        The policies are returned in two collections, one containing Conditional Access policies that require an
        MFA claim and the other containing Conditional Access policies that do not require such a claim.
        Policies in the former category are restricted in what kinds of changes may be made to them to prevent
        undermining the MFA requirement of those policies.
        """
        return_type = ClientResult(self.context, AuthenticationStrengthUsage())
        qry = FunctionQuery(self, "usage", None, return_type)
        self.context.add_query(qry)
        return return_type

    def update_allowed_combinations(
        self, allowed_combinations: List[str] | None = None
    ) -> ClientResult[UpdateAllowedCombinationsResult]:
        """Update the allowedCombinations property of an authenticationStrengthPolicy object.
        To update other properties of an authenticationStrengthPolicy object,
        use the Update authenticationStrengthPolicy method.

        Args:
            allowed_combinations (list[str]): The authentication method combinations allowed by this authentication
              strength policy.
        """
        return_type = ClientResult(self.context, UpdateAllowedCombinationsResult())
        payload = {"allowedCombinations": allowed_combinations}
        qry = ServiceOperationQuery(self, "updateAllowedCombinations", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def allowed_combinations(self) -> ClientValueCollection[AuthenticationMethodModes]:
        """Gets the allowedCombinations property"""
        return self.properties.get(
            "allowedCombinations", ClientValueCollection[AuthenticationMethodModes](AuthenticationMethodModes)
        )

    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def modified_date_time(self) -> Optional[datetime]:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def policy_type(self) -> AuthenticationStrengthPolicyType:
        """Gets the policyType property"""
        return self.properties.get("policyType", AuthenticationStrengthPolicyType.builtIn)

    @property
    def requirements_satisfied(self) -> AuthenticationStrengthRequirements:
        """Gets the requirementsSatisfied property"""
        return self.properties.get("requirementsSatisfied", AuthenticationStrengthRequirements.none)

    @property
    def combination_configurations(self) -> EntityCollection[AuthenticationCombinationConfiguration]:
        """Gets the combinationConfigurations property"""
        return self.properties.get(
            "combinationConfigurations",
            EntityCollection[AuthenticationCombinationConfiguration](
                self.context,
                AuthenticationCombinationConfiguration,
                ResourcePath("combinationConfigurations", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationStrengthPolicy"
