import logging

import office365.migration.assessment.scanners.list
from office365.migration.assessment.scanners.site import SiteScanner
from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_user_credentials

logging.basicConfig(
    level=logging.INFO,
)


ctx = ClientContext(test_team_site_url).with_credentials(test_user_credentials)
# lib = ctx.web.default_document_library()
# scanner = ListScanner(lib)

scanner = SiteScanner(ctx.site)
scan_info = scanner.scan()

logging.info(
    "Site_Usage %s",
    scan_info.properties,
)
