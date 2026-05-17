from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_client_credentials,
    test_team_site_url,
)

tenant = Tenant.from_url(test_admin_site_url).with_credentials(test_client_credentials)

result = tenant.get_site_secondary_administrators_by_site_url(test_team_site_url).execute_query()
# tenant.clear_site_secondary_administrators(test_team_site_url).execute_query()


user_result = tenant.context.search_user("SharePoint Service Administrator").execute_query()
names = [admin.loginName for admin in result.value] + [user_result.value.get("loginName")]
tenant.set_site_secondary_administrators_by_site_url(site_url=test_team_site_url, names=names).execute_query()
