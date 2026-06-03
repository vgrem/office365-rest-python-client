"""
List subject rights requests in Microsoft Purview.

Subject rights requests (SRR) help manage data subject requests under
regulations like GDPR, CCPA, and others.

Requires delegated permission ``SubjectRightsRequest.Read.All`` or
``SubjectRightsRequest.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-subjectrightsrequests?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

requests = client.security.subject_rights_requests.get().execute_query()
for req in requests:
    print(f"  {req.display_name:50s}  status: {req.status}")
