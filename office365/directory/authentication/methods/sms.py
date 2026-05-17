from office365.directory.authentication.methods.configuration import (
    AuthenticationMethodConfiguration,
)
from office365.directory.authentication.methods.sms_target import (
    SmsAuthenticationMethodTarget,
)
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class SmsAuthenticationMethodConfiguration(AuthenticationMethodConfiguration):
    """Represents a text message authentication methods policy. Authentication methods policies define
    configuration settings and users or groups that are enabled to use the authentication method.
    """

    @property
    def include_targets(self):
        """Groups of users that are excluded from the policy."""
        return self.properties.get(
            "includeTargets",
            EntityCollection(
                self.context,
                SmsAuthenticationMethodTarget,
                ResourcePath("includeTargets", self.resource_path),
            ),
        )
