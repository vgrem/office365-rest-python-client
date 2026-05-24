"""
Demonstrates how to copy a file within a site
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

file_from = ctx.web.get_file_by_server_relative_url("Shared Documents/Financial Sample.xlsx")
folder_to_url = "Shared Documents/archive"
new_filename = "Financial 2023.xlsx"
file_to = file_from.copyto(folder_to_url, True, new_filename).execute_query()
print(f"File copied into '{file_to.server_relative_url}'")
