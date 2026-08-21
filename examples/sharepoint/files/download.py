"""
Demonstrates how to download a file from SharePoint site
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Download a file from a SharePoint site")
    parser.add_argument("--file-url", default="Shared Documents/report '123.csv", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(args.file_url))
    with open(download_path, "wb") as local_file:
        ctx.web.get_file_by_server_relative_path(args.file_url).download(local_file).execute_query()
        print(f"[Ok] file has been downloaded into: {download_path}")


if __name__ == "__main__":
    main()
