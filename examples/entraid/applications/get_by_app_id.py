"""
Manage an Azure AD application using Microsoft Graph

https://learn.microsoft.com/en-us/graph/tutorial-applications-basics

You can address an application or a service principal by its ID or by its appId, where ID is referred to
as Object ID and appId is referred to as Application (client) ID on the Azure portal.

Requires delegated permission ``Application.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
app = client.applications.get_by_app_id(client_id).get().execute_query()
print(app)
