from office365.directory.authentication.methods.excludetarget import ExcludeTarget
from office365.directory.authentication.methods.state import AuthenticationMethodState
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection


class AuthenticationMethodConfiguration(Entity):
    """
    This is an abstract type that represents the settings for each authentication method. It has the configuration
    of whether a specific authentication method is enabled or disabled for the tenant and which users and groups
    can register and use that method.
    """

    @property
    def exclude_targets(self) -> ClientValueCollection[ExcludeTarget]:
        """Gets the excludeTargets property"""
        return self.properties.get("excludeTargets", ClientValueCollection[ExcludeTarget](ExcludeTarget))

    @property
    def state(self) -> AuthenticationMethodState:
        """Gets the state property"""
        return self.properties.get("state", AuthenticationMethodState.enabled)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationMethodConfiguration"
