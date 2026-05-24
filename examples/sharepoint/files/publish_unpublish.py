"""
Publish or unpublish a file for content approval.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/report.docx"
file = ctx.web.get_file_by_server_relative_path(file_url)

file.publish("Approved for team").execute_query()
print("File published")

# Later: unpublish
# file.unpublish("Needs revision").execute_query()
# print("File unpublished")
