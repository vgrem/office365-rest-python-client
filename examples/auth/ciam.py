"""
Connect via a custom MSAL authority — Microsoft Entra External ID (CIAM).

Uses the tenant's CIAM authority (https://<tenant>.ciamlogin.com).

https://learn.microsoft.com/en-us/entra/external-id/customers/overview
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

authority = f"https://{tenant}.ciamlogin.com"
client = GraphClient(tenant=tenant, authority=authority).with_client_secret(client_id, client_secret)

org = client.organization.get().execute_query()
for o in org:
    print(f"Organization: {o.properties.get('displayName')}")
