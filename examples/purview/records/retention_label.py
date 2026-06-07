"""
Create a retention label with retention period, record behavior,
and post-action disposition.

Retention labels define how long content is kept and what action
to take after the retention period expires.

Requires delegated permission ``RecordsManagement.ReadWrite.All``
and the Records Management administrator role.

https://learn.microsoft.com/en-us/graph/api/security-post-retentionlabels
"""

from office365.directory.security.labels.retention.actionafterretentionperiod import (
    ActionAfterRetentionPeriod,
)
from office365.directory.security.labels.retention.behaviorduringretentionperiod import (
    BehaviorDuringRetentionPeriod,
)
from office365.directory.security.labels.retention.defaultrecordbehavior import (
    DefaultRecordBehavior,
)
from office365.directory.security.labels.retention.duration_in_days import (
    RetentionDurationInDays,
)
from office365.directory.security.labels.retention.trigger import RetentionTrigger
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

label = client.security.labels.retention_labels.add(
    "Retain 1 Year — Delete",           # display_name
    RetentionTrigger.dateLabeled,         # retention_trigger
    RetentionDurationInDays(365),         # retention_duration
    BehaviorDuringRetentionPeriod.retainAsRecord,  # behavior_during_retention
    DefaultRecordBehavior.startLocked,    # default_record_behavior
    ActionAfterRetentionPeriod.delete,    # action_after_retention
).execute_query()

print(f"Label created: {label.display_name}")
print(f"  Trigger: {label.retention_trigger}")
print(f"  Action: {label.action_after_retention}")
print(f"  Retention days: {label.retention_duration_days}")
