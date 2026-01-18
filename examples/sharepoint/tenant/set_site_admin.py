from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_client_credentials,
    test_team_site_url,
    test_user_principal_name_alt,
)

tenant = Tenant.from_url(test_admin_site_url).with_credentials(test_client_credentials)

result = tenant.get_site_secondary_administrators_by_site_url(test_team_site_url).execute_query()
# tenant.clear_site_secondary_administrators(test_team_site_url).execute_query()

emails = [admin.email for admin in result.value] + [test_user_principal_name_alt]
tenant.set_site_secondary_administrators_by_site_url(site_url=test_team_site_url, emails=emails).execute_query()
