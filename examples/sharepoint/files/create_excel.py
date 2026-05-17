"""
Demonstrates how to create an Excel file in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
result = ctx.web.default_document_library().create_document_with_default_name("", "xlsx").execute_query()
print(f"'{result.value}' file has been created")
