"""
Run an advanced hunting KQL query against Microsoft 365 Defender data.

Queries tables such as AlertInfo, DeviceProcessEvents, EmailEvents,
IdentityLogonEvents, and more.

Requires delegated permission ``ThreatHunting.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-security-runhuntingquery
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
query = """
AlertInfo
| where Severity =~ "High"
| project Timestamp, AlertId, Title, Severity
| limit 2"""

result = client.security.run_hunting_query(query).execute_query()
print(result.value)
