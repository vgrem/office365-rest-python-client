"""
Retrieves versions of the file
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "SitePages/Home.aspx"
file_with_versions = ctx.web.get_file_by_server_relative_path(file_url).expand(["Versions"]).get().execute_query()

for version in file_with_versions.versions:
    # print(version.properties.get("Created"))
    print(version.version_label)
