from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.directory.authentication.fraud_protection_provider import (
        FraudProtectionProvider,
    )


@value
class FraudProtectionProviderConfiguration(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FraudProtectionProviderConfiguration"

    fraudProtectionProvider: FraudProtectionProvider | None = None
