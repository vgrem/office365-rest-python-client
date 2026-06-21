"""
Create a retention label with retention period, record behavior,
and post-action disposition.

Requires delegated permission ``RecordsManagement.ReadWrite.All``
and the Records Management administrator role.

https://learn.microsoft.com/en-us/graph/api/security-post-retentionlabels
"""

from office365.directory.security.labels.retention.actionafterretentionperiod import ActionAfterRetentionPeriod
from office365.directory.security.labels.retention.behaviorduringretentionperiod import BehaviorDuringRetentionPeriod
from office365.directory.security.labels.retention.defaultrecordbehavior import DefaultRecordBehavior
from office365.directory.security.labels.retention.duration_in_days import RetentionDurationInDays
from office365.directory.security.labels.retention.trigger import RetentionTrigger
from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Compliance Administrator")
)

label = client.security.labels.retention_labels.add(
    "Retain 1 Year — Delete v2",
    RetentionTrigger.dateLabeled,
    RetentionDurationInDays(365),
    BehaviorDuringRetentionPeriod.retainAsRecord,
    DefaultRecordBehavior.startLocked,
    ActionAfterRetentionPeriod.delete,
).execute_query()

print(f"Label created: {label.display_name}")
print(f"  Trigger: {label.retention_trigger}")
print(f"  Action: {label.action_after_retention_period}")
print(f"  Default behavior: {label.default_record_behavior}")
print(f"  In use: {label.is_in_use}")

duration = label.retention_duration
if duration:
    print(f"  Duration days: {duration.days if hasattr(duration, 'days') else duration}")
