from typing import Optional

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.webs.web import Web
from tests import test_client_credentials, test_team_site_url


def try_get_file(web, url):
    # type: (Web, str) -> Optional[File]
    try:
        return (
            web.get_file_by_server_relative_url(url)
            .select(["Exists"])
            .get()
            .execute_query()
        )
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
file_url = "Shared Documents/Financial Sample.xlsx"
file = try_get_file(ctx.web, file_url)
if file is None:
    print("File not found")
