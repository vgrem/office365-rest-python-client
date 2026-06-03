"""
List MFA registration status and authentication methods for all users.

Does not include disabled users.

Requires delegated permission ``AuditLog.Read.All`` or
``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

result = client.reports.authentication_methods.user_registration_details.get().execute_query()
for details in result:
    print(f"{details.user_principal_name}: {details.is_mfa_registered}")
