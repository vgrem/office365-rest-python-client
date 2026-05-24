"""
Demonstrates how to create a Word document in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
result = ctx.web.default_document_library().create_document_with_default_name("", "docx").execute_query()
print(f"'{result.value}' file has been created")
