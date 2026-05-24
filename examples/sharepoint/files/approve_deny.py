"""
Approve or deny a file submitted for content approval.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/report.docx"
file = ctx.web.get_file_by_server_relative_path(file_url)

file.approve("Looks good").execute_query()
print("File approved")

# Or deny:
# file.deny("Does not meet standards").execute_query()
# print("File denied")
