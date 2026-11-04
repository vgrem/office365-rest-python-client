from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomerKeyStatusInfo(ClientValue):
    AvailabilityKeyVaultUri: str | None = None
    PrimaryKeyVaultUri: str | None = None
    RecoveryEnabled: bool | None = None
    RegistrationProgress: float | None = None
    SecondaryKeyVaultUri: str | None = None
    Status: int | None = None
