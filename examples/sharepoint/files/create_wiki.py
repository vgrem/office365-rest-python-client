"""
Demonstrates how to create and delete a wiki page in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.pages.template_file_type import TemplateFileType
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
parent_folder = ctx.web.default_document_library().root_folder

file_url = "WikiPage 123.aspx"
file = parent_folder.files.add_template_file(file_url, TemplateFileType.WikiPage).execute_query()

file.delete_object().execute_query()
