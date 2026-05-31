from office365.directory.authentication.configuration_base import ApiAuthenticationConfigurationBase
from typing import Optional

class BasicAuthentication(ApiAuthenticationConfigurationBase):
    password: str | None = None
    username: str | None = None
    '\n    Represents configuration for using HTTP Basic authentication, which entails a username and password, in an API call.\n     The username and password is sent as the Authorization header as Basic {value} where value is\n     base 64 encoded version of username:password.\n    '

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.BasicAuthentication'