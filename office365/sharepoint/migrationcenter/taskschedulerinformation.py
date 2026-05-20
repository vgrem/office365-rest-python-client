from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TaskSchedulerInformation(ClientValue):
    AverageDurationMilliSeconds: Optional[int] = None
    CreatedDateUtc: Optional[str] = None
    DeliveryDateUtc: Optional[str] = None
    MaxDurationMilliSeconds: Optional[int] = None
    ScheduledTimes: Optional[int] = None
    SchedulerExists: Optional[bool] = None
    SchedulerId: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.TaskSchedulerInformation"
