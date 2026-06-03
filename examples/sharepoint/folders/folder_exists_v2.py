"""
How to determine whether a folder exists.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from http import HTTPStatus

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

folder_path = "SitePages"
ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
try:
    ctx.web.get_folder_by_server_relative_url(folder_path).get().execute_query()
    print(f"Folder '{folder_path}' is found")
except ClientRequestException as e:
    assert e.response is not None
    if e.response.status_code == HTTPStatus.NOT_FOUND:
        print("Folder '{0}' not found".format(folder_path))
    else:
        raise ValueError(e.response.text) from e
