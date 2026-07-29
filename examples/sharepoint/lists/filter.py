"""Demonstrates how to apply OData filtering to a list collection

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

ctx = ClientContext(team_site_url).with_username_and_password(tenant, client_id, username, password)
result = ctx.web.lists.get().select(["IsSystemList", "Title"]).filter("IsSystemList eq false").execute_query()
for lst in result:
    print(lst.title)
