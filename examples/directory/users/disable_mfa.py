"""
Disable MFA
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

methods = client.me.authentication.microsoft_authenticator_methods.get().execute_query()
for method in methods:
    method.delete_object().execute_query()
