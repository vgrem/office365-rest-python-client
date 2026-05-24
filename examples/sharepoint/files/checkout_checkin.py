"""
Check out a file, edit it, and check it back in.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.checkin_type import CheckinType
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/draft.docx"
file = ctx.web.get_file_by_server_relative_path(file_url)

file.checkout().execute_query()
print("File checked out")

# Edit the file content
content = b"Updated content"
file.save_binary_stream(content).execute_query()

file.checkin("Updated via API", CheckinType.MajorCheckIn).execute_query()
print("File checked in")
