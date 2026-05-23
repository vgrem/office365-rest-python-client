"""
Shares a web with a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.external_site_option import ExternalSharingSiteOption
from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_user_principal_name_alt,
    test_username,
)

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

result = ctx.web.share(test_user_principal_name_alt, ExternalSharingSiteOption.View).execute_query()
if result.error_message is not None:
    sys.exit("Web sharing failed: {0}".format(result.error_message))

print(f"Web '{result.url}' has been shared with user '{test_user_principal_name_alt}'")
