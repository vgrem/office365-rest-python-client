"""
Revoke an app role assignment from a client service principal

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

client.revoke_application_permissions(client_id, "MailboxSettings.Read").execute_query()
