from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from office365.directory.authentication.fraud_protection_provider import (
        FraudProtectionProvider,
    )


class FraudProtectionProviderConfiguration(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FraudProtectionProviderConfiguration"

    fraudProtectionProvider: FraudProtectionProvider | None = None
