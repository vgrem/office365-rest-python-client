"""
Gets site collection administrators
"""

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_credentials, test_team_site_url

tenant = Tenant.from_url(test_admin_site_url).with_credentials(test_client_credentials)

print("Primary Administrators:")
result = tenant.get_site_administrators_by_site_url(test_team_site_url).execute_query()
for admin in result.value:
    print(admin.loginName)

print("\nSecondary Administrators:")
result = tenant.get_site_secondary_administrators_by_site_url(test_team_site_url).execute_query()
for admin in result.value:
    print(admin.loginName)
