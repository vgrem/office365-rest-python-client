"""
Generates a site script from an existing list.

Site scripts can be generated from existing lists to capture
their configuration for reuse.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
target_list = ctx.web.default_document_library()
result = target_list.get_site_script().execute_query()
print(result.value)
