"""
Gets all sharing links and permissions for a file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

file_url = "Shared Documents/Financial Sample.xlsx"
file = ctx.web.get_file_by_server_relative_url(file_url)

info = file.get_sharing_information().execute_query()
print(f"Anonymous view link:    {info.anonymous_view_link}")
print(f"Anonymous edit link:    {info.anonymous_edit_link}")
print(f"Sharing links count:    {len(info.sharing_links)}")
for link in info.sharing_links:
    print(f"  - {link.Url}  (kind: {link.LinkKind})")
users = info.shared_with_users_collection
print(f"Users with access:      {len(users) if users else 0}")
