"""
Demonstrates how to retain the history for list items.
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
items = ctx.web.lists.get_by_title("Site Pages").items.expand(["Versions"]).get().top(10).execute_query()

for item in items:
    for version in item.versions:
        print(version)
