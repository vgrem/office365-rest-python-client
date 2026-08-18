"""
Get admin consent request policy.

Retrieves the policy that controls how users can request admin consent
for apps and whether reviewers are notified.

https://learn.microsoft.com/en-us/graph/api/adminconsentrequestpolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/adminconsentrequestpolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

policy = client.policies.admin_consent_request_policy.get().execute_query()

print(f"Is enabled: {policy.properties.get('isEnabled', False)}")
print(f"Notify reviewers: {policy.properties.get('notifyReviewers', False)}")
print(f" reviewers: {policy.properties.get('reviewersEmails', [])}")
