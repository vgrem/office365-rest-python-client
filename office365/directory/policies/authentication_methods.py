from datetime import datetime
from typing import Optional

from office365.directory.authentication.methods.configuration import AuthenticationMethodConfiguration
from office365.directory.authentication.methods.policymigrationstate import AuthenticationMethodsPolicyMigrationState
from office365.directory.authentication.methods.registrationenforcement import RegistrationEnforcement
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AuthenticationMethodsPolicy(Entity):
    """Defines authentication methods and the users that are allowed to use them to sign in and perform multi-factor
    authentication (MFA) in Azure Active Directory (Azure AD).
    """

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="policyMigrationState")
    @property
    def policy_migration_state(self) -> AuthenticationMethodsPolicyMigrationState:
        """Gets the policyMigrationState property"""
        return self.properties.get("policyMigrationState", AuthenticationMethodsPolicyMigrationState.preMigration)

    @odata(name="policyVersion")
    @property
    def policy_version(self) -> Optional[str]:
        """Gets the policyVersion property"""
        return self.properties.get("policyVersion", None)

    @odata(name="reconfirmationInDays")
    @property
    def reconfirmation_in_days(self) -> Optional[int]:
        """Gets the reconfirmationInDays property"""
        return self.properties.get("reconfirmationInDays", None)

    @odata(name="registrationEnforcement")
    @property
    def registration_enforcement(self) -> RegistrationEnforcement:
        """Gets the registrationEnforcement property"""
        return self.properties.get("registrationEnforcement", RegistrationEnforcement())

    @odata(name="authenticationMethodConfigurations", navigation=True)
    @property
    def authentication_method_configurations(self) -> EntityCollection[AuthenticationMethodConfiguration]:
        """Gets the authenticationMethodConfigurations property"""
        return self.properties.get(
            "authenticationMethodConfigurations",
            EntityCollection[AuthenticationMethodConfiguration](
                self.context,
                AuthenticationMethodConfiguration,
                ResourcePath("authenticationMethodConfigurations", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationMethodsPolicy"
