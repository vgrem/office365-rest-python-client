"""
Demonstrates how to retrieve the total count of users in the tenant.

https://learn.microsoft.com/en-us/graph/api/resources/user
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)


result = client.users.count().execute_query()
print(f"Total users: {result.value}")
