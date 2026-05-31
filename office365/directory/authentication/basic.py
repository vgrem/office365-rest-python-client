from __future__ import annotations

from office365.directory.authentication.configuration_base import ApiAuthenticationConfigurationBase


class BasicAuthentication(ApiAuthenticationConfigurationBase):
    password: str | None = None
    username: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BasicAuthentication"
