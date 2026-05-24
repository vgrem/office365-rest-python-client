"""
Demonstrates how to download a file using its absolute URL.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import os
import tempfile

from office365.sharepoint.files.file import File
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

abs_file_url = f"{test_site_url}/sites/team/Shared Documents/archive/big_buck_bunny.mp4"

with tempfile.TemporaryDirectory() as local_path:
    file_name = os.path.basename(abs_file_url)
    with open(os.path.join(local_path, file_name), "wb") as local_file:
        file = (
            File.from_url(abs_file_url)
            .with_client_secret(test_tenant, test_client_id, test_client_secret)
            .download(local_file)
            .execute_query()
        )
    print(f"'{file.server_relative_path}' file has been downloaded into {local_file.name}")
