"""
Sets secondary site collection administrators on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)

ctx = Tenant.from_url(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

result = ctx.get_site_secondary_administrators_by_site_url(test_team_site_url).execute_query()

user_result = ctx.context.search_user("SharePoint Service Administrator").execute_query()
names = [admin.loginName for admin in result.value if admin.loginName is not None]
user_name = user_result.value.get("loginName")
if user_name is not None:
    names.append(user_name)
ctx.set_site_secondary_administrators_by_site_url(site_url=test_team_site_url, names=names).execute_query()

