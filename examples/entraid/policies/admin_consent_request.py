"""
Get admin consent request policy.

Retrieves the policy that controls how users can request admin consent
for apps and whether reviewers are notified.

https://learn.microsoft.com/en-us/graph/api/adminconsentrequestpolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/adminconsentrequestpolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

policy = client.policies.admin_consent_request_policy.get().execute_query()

print(f"Is enabled: {policy.properties.get('isEnabled', False)}")
print(f"Notify reviewers: {policy.properties.get('notifyReviewers', False)}")
print(f" reviewers: {policy.properties.get('reviewersEmails', [])}")
