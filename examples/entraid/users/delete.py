"""
Delete a user.

Permanently deletes a user by user principal name (UPN).
Deleting a user moves it to the recycle bin; passing
``permanent_delete=True`` removes it immediately.

https://learn.microsoft.com/en-us/graph/api/user-delete

https://learn.microsoft.com/en-us/graph/api/resources/user

Requires delegated permission ``User.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

user = client.users.get_by_principal_name("user@contoso.onmicrosoft.com")
user.delete_object(permanent_delete=True).execute_query()
print("User deleted.")
