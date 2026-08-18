"""
List all subject rights requests.

Requires delegated permission ``SubjectRightsRequest.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-subjectrightsrequests
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

requests = client.security.subject_rights_requests.get().execute_query()
print(f"Subject rights requests ({len(requests)}):")
for r in requests:
    props = r.properties
    name = props.get("displayName", "(unnamed)")
    print(f"  {name:40s}  type={props.get('type', '?'):10s}  status={props.get('status', '?')}")
