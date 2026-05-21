from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class LicenseUnitsDetail(ClientValue):
    """LicenseUnitsDetail

    :param int enabled: The number of units that are enabled for the active subscription of the service SKU.
    """

    enabled: int | None = None
    lockedOut: int | None = None
    suspended: int | None = None
    warning: int | None = None
