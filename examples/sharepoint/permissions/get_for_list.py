"""
Return effective user permissions for a list or library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
doc_lib = ctx.web.default_document_library()
result = doc_lib.get_user_effective_permissions(ctx.web.current_user).execute_query()
for perm_level in result.value:
    print(perm_level)
