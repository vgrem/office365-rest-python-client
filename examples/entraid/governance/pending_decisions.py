"""
List access review decisions pending review for the current user.

Shows reviews where the current user is a reviewer and decisions
are still pending.

Requires delegated permission ``AccessReview.Read.All``.

https://learn.microsoft.com/en-us/graph/api/accessreviewinstance-list-decisions
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

response = client.execute_request_get(
    "/identityGovernance/accessReviews/definitions?$select=id,displayName,status&$top=10"
)
for d in response.json().get("value", []):
    defn_id = d["id"]
    instances = client.execute_request_get(
        f"/identityGovernance/accessReviews/definitions/{defn_id}/instances?$filter=status eq 'inProgress'&$select=id"
    )
    for inst in instances.json().get("value", []):
        decisions = client.execute_request_get(
            f"/identityGovernance/accessReviews/definitions/{defn_id}/instances/{inst['id']}/decisions"
        )
        for dec in decisions.json().get("value", []):
            if dec.get("decision") == "NotReviewed":
                principal = dec.get("principal", {}).get("userPrincipalName", "?")
                print(f"  {d['displayName']:40s}  user={principal}")
