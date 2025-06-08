import logging

from office365.migration.assessment.list_scanner import ListScanner
from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_user_credentials

logging.basicConfig(
    level=logging.INFO,
)


ctx = ClientContext(test_team_site_url).with_credentials(test_user_credentials)
lib = ctx.web.default_document_library()
scanner = ListScanner(lib)
scan_info = scanner.scan()
logging.info(
    "List_Usage %s",
    scan_info,
)
