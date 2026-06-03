"""
Get the Microsoft Secure Score control profiles.

Shows the current score and improvement actions for the tenant.

Requires delegated permission ``SecurityEvents.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-securescorecontrolprofiles?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

profiles = client.security.secure_score_control_profiles.get().execute_query()
for profile in profiles:
    score = profile.max_score or 0
    print(f"  {profile.title:50s}  max score: {score}")
