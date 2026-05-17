"""
Creates a modern team site (Microsoft 365 group-connected).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_site_url, test_user_credentials

alias = create_unique_name("teamsite")
title = "Team Site"
ctx = ClientContext(test_site_url).with_credentials(test_user_credentials)
site = ctx.create_team_site(alias, title).execute_query()
print(site.url)

site.delete_object().execute_query()  # cleanup: remove resource
