from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.authentication.externalemailotpstate import ExternalEmailOtpState
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.methods.target import (
        AuthenticationMethodTarget,
    )


class EmailAuthenticationMethodConfiguration(Entity):
    @odata(name="allowExternalIdToUseEmailOtp")
    @property
    def allow_external_id_to_use_email_otp(self) -> ExternalEmailOtpState:
        """Gets the allowExternalIdToUseEmailOtp property"""
        return self.properties.get("allowExternalIdToUseEmailOtp", ExternalEmailOtpState.default)

    @odata(name="includeTargets", navigation=True)
    @property
    def include_targets(self) -> EntityCollection[AuthenticationMethodTarget]:
        """Gets the includeTargets property"""
        from office365.directory.authentication.methods.target import (
            AuthenticationMethodTarget,
        )

        return self.properties.get(
            "includeTargets",
            EntityCollection[AuthenticationMethodTarget](
                self.context, AuthenticationMethodTarget, ResourcePath("includeTargets", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailAuthenticationMethodConfiguration"
