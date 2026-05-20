from __future__ import annotations

import datetime
from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UpgradeInfo(ClientValue):
    """A class containing site collection upgrade information.

    Fields:
        ErrorFile: Specifies the location of the file that contains upgrade errors.
        Errors: Specifies the number of errors encountered during the site collection upgrade.
        LastUpdated: Specifies the DateTime of the latest upgrade progress update.
        LogFile: Specifies the location of the file that contains upgrade log.
        RequestDate: Specifies the DateTime when the site collection upgrade was requested.
        RetryCount: Specifies how many times the site collection upgrade was attempted.
        StartTime: Specifies the DateTime when the site collection upgrade was started.
        Status: Specifies the current site collection upgrade status.
        UpgradeType: Specifies the type of the site collection upgrade type. The type can be either a
            build-to-build upgrade, or a version-to-version upgrade.
        Warnings: Specifies the number of warnings encountered during the site collection upgrade.
    """

    ErrorFile: str | None = None
    Errors: int | None = None
    LastUpdated: datetime.datetime = datetime.datetime.min
    LogFile: str | None = None
    RequestDate: datetime.datetime = datetime.datetime.min
    RetryCount: int | None = None
    StartTime: datetime.datetime = datetime.datetime.min
    Status: int | None = None
    UpgradeType: int | None = None
    Warnings: int | None = None
