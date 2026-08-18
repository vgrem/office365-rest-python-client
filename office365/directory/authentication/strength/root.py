from office365.directory.authentication.methods.mode_detail import AuthenticationMethodModeDetail
from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.directory.policies.authentication_strength import AuthenticationStrengthPolicy
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath


class AuthenticationStrengthRoot(Entity):
    """The authenticationStrengthRoot resource is the entry point for the authentication strengths object model."""

    @property
    def combinations(self) -> ClientValueCollection[AuthenticationMethodModes]:
        """Gets the combinations property"""
        return self.properties.get(
            "combinations", ClientValueCollection[AuthenticationMethodModes](AuthenticationMethodModes)
        )

    @property
    def authentication_method_modes(self) -> EntityCollection[AuthenticationMethodModeDetail]:
        """Gets the authenticationMethodModes property"""
        return self.properties.get(
            "authenticationMethodModes",
            EntityCollection[AuthenticationMethodModeDetail](
                self.context,
                AuthenticationMethodModeDetail,
                ResourcePath("authenticationMethodModes", self.resource_path),
            ),
        )

    @property
    def policies(self) -> EntityCollection[AuthenticationStrengthPolicy]:
        """Gets the policies property"""
        return self.properties.get(
            "policies",
            EntityCollection[AuthenticationStrengthPolicy](
                self.context, AuthenticationStrengthPolicy, ResourcePath("policies", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationStrengthRoot"
