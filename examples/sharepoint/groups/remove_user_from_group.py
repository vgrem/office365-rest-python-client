"""Demonstrates how to remove a user from a SharePoint group.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
group = ctx.web.site_groups.get_by_name("Team Site Members")
group.users.remove_by_login_name("i:0#.f|membership|user@contoso.com").execute_query()
print("User removed")