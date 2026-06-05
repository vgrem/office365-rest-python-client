"""
Demonstrates how to check if a file exists on a SharePoint site.

Attempts to retrieve a file by its server-relative URL and returns None if not found.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_cert_path, test_cert_thumbprint, test_client_id, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_certificate(
    test_tenant, client_id=test_client_id, thumbprint=test_cert_thumbprint, cert_path=test_cert_path
)
file_url = "/Shared Documents/Financial Sample11.xlsx"
result = ctx.web.get_file_by_server_relative_url(file_url).get_exists().execute_query()
if result.value:
    print(f"File '{file_url}' exists.")
else:
    print(f"File '{file_url}' not found.")
