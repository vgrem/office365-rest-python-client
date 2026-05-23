"""
Creates a modern team site (Microsoft 365 group-connected).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_client_id, test_password, test_site_url, test_tenant, test_username

alias = create_unique_name("teamsite")
title = "Team Site"
ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
site = ctx.create_team_site(alias, title).execute_query()
print(site.url)

site.delete_object().execute_query()  # cleanup: remove resource
