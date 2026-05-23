"""
Resolves a web from an absolute resource (e.g. page) URL.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

page_abs_url = "{site_url}/SitePages/Home.aspx".format(site_url=test_team_site_url)
ctx = ClientContext.from_url(page_abs_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
web = ctx.web.get().execute_query()
print(web.url)
