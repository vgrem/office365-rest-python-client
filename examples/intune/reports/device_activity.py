"""
Reports: device configuration activity and enrollment failure details.

Provides adoption and troubleshooting insights — how many devices
are configured and what enrollment errors exist.

Requires delegated permission ``DeviceManagementConfiguration.Read.All``
and ``DeviceManagementManagedDevices.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-reportroot
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = (
    GraphClient(tenant=test_tenant)
    .with_client_secret(test_client_id, test_client_secret)
    .require_application_permission("DeviceManagementConfiguration.Read.All")
)

# 1. Device configuration user activity
user_activity = client.reports.device_configuration_user_activity().execute_query()
print(f"Device config user activity: {user_activity.value}")

# 2. Device configuration device activity
device_activity = client.reports.device_configuration_device_activity().execute_query()
print(f"Device config device activity: {device_activity.value}")

# 3. Enrollment failure details
failures = client.reports.managed_device_enrollment_failure_details().execute_query()
print(f"Enrollment failure details: {failures.value}")

# 4. Top enrollment failures
top_failures = client.reports.managed_device_enrollment_top_failures().execute_query()
print(f"Top enrollment failures: {top_failures.value}")
