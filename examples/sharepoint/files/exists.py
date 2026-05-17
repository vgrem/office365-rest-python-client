"""
Demonstrates how to check if a file exists on a SharePoint site.

Attempts to retrieve a file by its server-relative URL and returns None if not found.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from http import HTTPStatus
from typing import Optional

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.webs.web import Web
from tests import test_client_credentials, test_team_site_url


def try_get_file(web: Web, url: str) -> Optional[File]:
    try:
        return web.get_file_by_server_relative_url(url).select(["Exists"]).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == HTTPStatus.NOT_FOUND:
            return None
        else:
            raise ValueError(e.response.text) from e


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
file_url = "Shared Documents/Financial Sample.xlsx"
file = try_get_file(ctx.web, file_url)
if file is None:
    print("File not found")
