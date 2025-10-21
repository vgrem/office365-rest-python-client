import logging

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.migration.assessment.scanners.site import SiteScanner
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

logging.basicConfig(
    level=logging.INFO,
)


ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
# lib = ctx.web.default_document_library()
# scanner = ListScanner(lib)

scanner = SiteScanner(ctx.site)
scan_info = scanner.scan()

logging.info(
    "Site_Usage %s",
    scan_info.properties,
)
