from typing import Optional

from office365.runtime.client_value import ClientValue


class TaskSchedulerInformation(ClientValue):
    def __init__(
        self,
        average_duration_milli_seconds: Optional[int] = None,
        created_date_utc: Optional[str] = None,
        delivery_date_utc: Optional[str] = None,
        max_duration_milli_seconds: Optional[int] = None,
        scheduled_times: Optional[int] = None,
        scheduler_exists: Optional[bool] = None,
        scheduler_id: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.AverageDurationMilliSeconds = average_duration_milli_seconds
        self.CreatedDateUtc = created_date_utc
        self.DeliveryDateUtc = delivery_date_utc
        self.MaxDurationMilliSeconds = max_duration_milli_seconds
        self.ScheduledTimes = scheduled_times
        self.SchedulerExists = scheduler_exists
        self.SchedulerId = scheduler_id
        self.Version = version

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.TaskSchedulerInformation"
