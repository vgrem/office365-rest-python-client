"""
Get personal site for current user
"""

from office365.sharepoint.client_context import ClientContext
from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
my_site = ctx.web.current_user.get_personal_site().execute_query()
print(my_site.url)
