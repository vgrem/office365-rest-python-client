"""
Demonstrates how to download a file using its absolute URL.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download a file by absolute URL")
    parser.add_argument(
        "--url",
        default="https://contoso.sharepoint.com/sites/team/Shared%20Documents/archive/report.docx",
        help="absolute file URL",
    )
    args = parser.parse_args()

    ctx = ClientContext.from_url(args.url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file_name = os.path.basename(args.url).replace("%20", " ")
    file = ctx.web.get_file_by_server_relative_url(args.url.replace(ctx.base_url, ""))

    with tempfile.TemporaryDirectory() as tmp_dir:
        local_path = os.path.join(tmp_dir, file_name)
        with open(local_path, "wb") as local_file:
            file.download(local_file).execute_query()
        print(f"'{file.server_relative_path}' file has been downloaded into {local_path}")


if __name__ == "__main__":
    main()
