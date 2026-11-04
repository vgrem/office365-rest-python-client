from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_overwrite_configuration import (
    CustomExtensionOverwriteConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.directory.identities.on_token_issuance_start_custom_extension import (
        OnTokenIssuanceStartCustomExtension,
    )


@value
class OnTokenIssuanceStartCustomExtensionHandler(ClientValue):
    configuration: CustomExtensionOverwriteConfiguration = field(default_factory=CustomExtensionOverwriteConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnTokenIssuanceStartCustomExtensionHandler"

    customExtension: OnTokenIssuanceStartCustomExtension | None = None
