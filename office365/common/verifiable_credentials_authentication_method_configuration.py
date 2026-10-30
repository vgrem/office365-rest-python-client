from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.verifiable_credential_authentication_method_target import (
        VerifiableCredentialAuthenticationMethodTarget,
    )


class VerifiableCredentialsAuthenticationMethodConfiguration(Entity):
    @odata(name="includeTargets", navigation=True)
    @property
    def include_targets(self) -> EntityCollection[VerifiableCredentialAuthenticationMethodTarget]:
        """Gets the includeTargets property"""
        from office365.common.verifiable_credential_authentication_method_target import (
            VerifiableCredentialAuthenticationMethodTarget,
        )

        return self.properties.get(
            "includeTargets",
            EntityCollection[VerifiableCredentialAuthenticationMethodTarget](
                self.context,
                VerifiableCredentialAuthenticationMethodTarget,
                ResourcePath("includeTargets", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VerifiableCredentialsAuthenticationMethodConfiguration"
