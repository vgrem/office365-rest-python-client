"""
Retrieves file check out status

https://support.microsoft.com/en-us/office/check-out-or-check-in-files-in-a-document-library-acce24cd-ab39-4fcf-9c4d-1ce3050dc602
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "SitePages/Home.aspx"
file = ctx.web.get_file_by_server_relative_url(file_url).get().execute_query()

if file.check_out_type == 0:
    print("The file is checked out for editing on the server")
elif file.check_out_type == 1:
    print("The file is checked out for editing on the local computer.")
else:
    print("The file is not checked out.")
