"""
Generates a site script from an existing site.

Site scripts can be exported from an existing site and reused
to apply the same configuration to other sites.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
result = ctx.web.get_site_script(included_lists=["Shared Documents"]).execute_query()
print(result.value.JSON)
