"""
Run a site migration assessment scan using the SharePoint Migration API.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import logging

from office365.migration.assessor import MigrationAssessor
from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

logging.basicConfig(
    level=logging.INFO,
)


ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)

report_result = MigrationAssessor(ctx.web).include_permissions().include_versions().assess().execute_query()

print(report_result.value.summary())
print(report_result.value.blockers)
