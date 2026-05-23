"""
Creates an anonymous sharing link for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

folder_url = "Shared Documents/Archive"
folder = ctx.web.get_folder_by_server_relative_url(folder_url)

result = folder.share_link(SharingLinkKind.AnonymousView).execute_query()
print(json.dumps(result.value.to_json(), indent=4))
print(f"Anonymous link: {result.value.sharingLinkInfo.Url}")
