"""
Create a team from an existing Microsoft 365 group.

Group-to-team provisioning is async — uses ``execute_query_retry``
with a retry callback to wait for Azure AD replication.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-put-teams?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)


def print_failure(retry_number, ex):
    print(f"  Attempt {retry_number}: Team provisioning still in progress...")


client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)
group_name = create_unique_name("Flight")
group = client.groups.create_m365(group_name)
team = group.add_team().execute_query_retry(
    max_retry=10, failure_callback=print_failure
)
print(f"Team created: {team.display_name}  ({team.web_url})")
