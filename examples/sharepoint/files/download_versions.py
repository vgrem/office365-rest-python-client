import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from tests import test_client_credentials, test_team_site_url


def download_file_versions(source_file: File, target_path: str):
    file_versions = source_file.versions.get().execute_query()
    for version in file_versions:
        with open(target_path, "wb") as f:
            version.download(f).execute_query()
        print(f"[Ok] file version {version.version_label} has been downloaded into: {target_path}")


def download_specific_file_version(source_file: File, version: int, target_path: str):
    version = source_file.versions.get_by_id(version)
    with open(target_path, "wb") as f:
        version.download(f).execute_query()
    print(f"[Ok] file version {version.url} has been downloaded into: {target_path}")


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
file_url = "SitePages/Home.aspx"
remote_file = ctx.web.get_file_by_server_relative_path(file_url)
local_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
download_file_versions(remote_file, local_path)
# download_specific_file_version(remote_file, 1, local_path)
