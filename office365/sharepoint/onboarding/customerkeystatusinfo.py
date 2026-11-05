from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CustomerKeyStatusInfo(ClientValue):
    AvailabilityKeyVaultUri: str | None = None
    PrimaryKeyVaultUri: str | None = None
    RecoveryEnabled: bool | None = None
    RegistrationProgress: float | None = None
    SecondaryKeyVaultUri: str | None = None
    Status: int | None = None
