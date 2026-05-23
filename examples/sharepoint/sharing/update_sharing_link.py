"""
Updates an existing sharing link (e.g. change expiration date).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from datetime import datetime, timedelta, timezone

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

file_url = "Shared Documents/Financial Sample.xlsx"
file = ctx.web.get_file_by_server_relative_url(file_url)

# Create a link that expires in 7 days
expires = datetime.now(timezone.utc) + timedelta(days=7)
result = file.share_link(SharingLinkKind.AnonymousView, expiration=expires).execute_query()
link_url = result.value.sharingLinkInfo.Url
print(f"Created link with 7-day expiry: {link_url}")

# Update the same link to expire in 30 days
expires = datetime.now(timezone.utc) + timedelta(days=30)
result = file.share_link(SharingLinkKind.AnonymousView, expiration=expires).execute_query()
print(f"Updated expiry to 30 days: {result.value.sharingLinkInfo.Url}")
