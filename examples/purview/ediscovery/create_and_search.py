"""
eDiscovery: full case workflow — create, add custodian, run search,
and close.

Shows the core eDiscovery (Premium) lifecycle in Microsoft Purview.

Requires delegated permission ``eDiscovery.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-post-ediscoverycases
https://learn.microsoft.com/en-us/graph/api/security-ediscoverycase-post-custodians
https://learn.microsoft.com/en-us/graph/api/security-ediscoverycase-post-searches
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_client_secret,
    test_tenant,
    test_user_principal_name,
)

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. Create an eDiscovery case
case_name = create_unique_name("SDK eDiscovery Case")
case = client.security.cases.ediscovery_cases.add(
    displayName=case_name,
    description="Investigation: data export review",
).execute_query()
print(f"Case created: {case.display_name}  (ID: {case.id})")

# 2. Add a custodian (user whose data is under review)
try:
    custodian = case.custodians.add(email=test_user_principal_name).execute_query()
    print(f"Custodian added: {custodian.display_name}")
except Exception as e:
    print(f"Custodian not added: {e}")

# 3. Create a search within the case
search = case.searches.add(
    displayName=create_unique_name("SDK Search"),
    contentQuery="subject:'confidential'",
).execute_query()
print(f"Search created: {search.display_name}")

# 4. Close and delete
case.delete_object().execute_query()
print("Case closed and deleted.")
