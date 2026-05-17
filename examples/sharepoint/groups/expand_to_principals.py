"""Expands a SharePoint group into a collection of principal information objects.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_team_site_url

ctx = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)

result = ctx.web.associated_member_group.expand_to_principals(100).execute_query()
for principal_info in result.value:
    print(principal_info)
