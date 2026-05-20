from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TimeZoneInformation(ClientValue):
    """Provides information used to define a time zone.

    Bias: Gets the bias in the number of minutes that the time zone differs from
        Coordinated Universal Time (UTC).
    DaylightBias: Gets the bias in the number of minutes that daylight time for the time zone
        differs from Coordinated Universal Time (UTC).
    StandardBias: Gets the bias in the number of minutes that standard time for the time zone differs
        from coordinated universal time (UTC).
    """

    Bias: Optional[int] = None
    DaylightBias: Optional[int] = None
    StandardBias: Optional[int] = None
