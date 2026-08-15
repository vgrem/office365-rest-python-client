"""
Gets primary and secondary site collection administrators for a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_team_site_url
from tests.settings import cert_path, cert_thumbprint, client_id, tenant

tenant = Tenant.from_url(test_admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

print("Primary Administrators:")
result = tenant.get_site_administrators_by_site_url(test_admin_site_url).execute_query()
for admin in result.value:
    print(admin.loginName)

print("\nSecondary Administrators:")
result = tenant.get_site_secondary_administrators_by_site_url(test_team_site_url).execute_query()
for admin in result.value:
    print(admin.loginName)
