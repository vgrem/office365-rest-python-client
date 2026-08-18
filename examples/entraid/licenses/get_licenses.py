"""
Retrieve a list of licenseDetails objects for the signed-in user.

Requires delegated permission ``User.Read`` (or ``User.Read.All``);
``/me`` is a delegated API.

https://learn.microsoft.com/en-us/graph/api/user-list-licensedetails
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = (
    GraphClient(tenant=tenant)
    .with_username_and_password(client_id, username, password)
    .require_delegated_permission("User.Read", "User.Read.All", "User.ReadWrite.All")
)
result = client.me.license_details.get().execute_query()
for details in result:
    print(details)
