"""
eDiscovery: full case workflow — create, add custodian, run search,
and close.

Requires delegated permission ``eDiscovery.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-post-ediscoverycases
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant, user_principal

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

case_name = create_unique_name("SDK eDiscovery Case")
case = client.security.cases.ediscovery_cases.add(
    displayName=case_name,
    description="Investigation: data export review",
).execute_query()
print(f"Case created: {case.display_name}  (ID: {case.id})")

try:
    custodian = case.custodians.add(email=user_principal).execute_query()
    print(f"Custodian added: {custodian.display_name}")
except Exception as e:
    print(f"Custodian not added: {e}")

search = case.searches.add(
    displayName=create_unique_name("SDK Search"),
    contentQuery="subject:'confidential'",
).execute_query()
print(f"Search created: {search.display_name}")

case.delete_object().execute_query()
print("Case closed and deleted.")
