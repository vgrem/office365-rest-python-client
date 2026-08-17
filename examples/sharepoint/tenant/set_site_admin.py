"""
Sets secondary site collection administrators on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = Tenant.from_url(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

result = ctx.get_site_secondary_administrators_by_site_url(team_site_url).execute_query()

user_result = ctx.context.search_user("SharePoint Service Administrator").execute_query()
names = [admin.loginName for admin in result.value if admin.loginName is not None]
user_name = user_result.value.get("loginName")
if user_name is not None:
    names.append(user_name)
ctx.set_site_secondary_administrators_by_site_url(site_url=team_site_url, names=names).execute_query()
