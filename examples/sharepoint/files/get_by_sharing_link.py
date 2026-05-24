"""
Gets file by shared link
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# Generate sharing link url for a file first
file = ctx.web.get_file_by_server_relative_url("/sites/team/SitePages/How To Use This Library.aspx")
# Share a file
result = file.share_link(SharingLinkKind.OrganizationView).execute_query()

# Resolve file by sharing link url (guest url)
file = ctx.web.get_file_by_guest_url(str(result.value)).execute_query()
print(file)
