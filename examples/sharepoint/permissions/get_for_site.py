"""
Return effective user permissions for a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from pprint import pprint

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
result = ctx.web.get_user_effective_permissions(ctx.web.current_user).execute_query()
pprint(result.value.permission_levels)  # type: ignore[attr-defined]
