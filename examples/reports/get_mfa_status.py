"""
List MFA registration status for all users.

Shows which users have MFA registered, authentication methods,
and capabilities.

Requires delegated permission ``AuditLog.Read.All`` or
``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

result = client.reports.authentication_methods.user_registration_details.get().execute_query()
print(f"{'User':40s}  {'MFA':6s}  {'Methods'}")
print("-" * 70)
for details in result:
    methods = ", ".join(details.methods or []) if details.methods else ""
    print(f"{details.user_principal_name:40s}  {str(details.is_mfa_registered):6s}  {methods}")
