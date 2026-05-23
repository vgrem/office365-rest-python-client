"""
Creates a modern communication site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from random import randint

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
alias = str(randint(0, 10000))
title = "Communication Site"
site = ctx.create_communication_site(alias, title).execute_query()
print(site.url)

print("Cleaning up resources...")
site.delete_object().execute_query()
