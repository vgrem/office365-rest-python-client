"""
This example specifies a KQL query which does the following:

   - Looks into the AlertInfo table in the advanced hunting schema.
   - Filters on alerts with high severity.
   - Projects selected columns.
   - Limits the output to 2 records.

https://learn.microsoft.com/en-us/graph/api/resources/security-api-overview
https://learn.microsoft.com/en-us/graph/api/security-security-runhuntingquery?view=graph-rest-1.0
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
