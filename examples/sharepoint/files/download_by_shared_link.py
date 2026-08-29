"""
Demonstrates how to download a file using a sharing link (guest URL).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download a file using a sharing link (guest URL)")
    parser.add_argument(
        "--sharing-link",
        default="https://mediadev8.sharepoint.com/:x:/s/team/EcEbi_M2xQJLng_bvQjPtgoB1rB6BFvMVFixnf4wOxfE5w?e=bzNjb6",
        help="file sharing link",
    )
    args = parser.parse_args()

    client = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    download_path = os.path.join(tempfile.mkdtemp(), "Report.csv")
    with open(download_path, "wb") as local_file:
        client.web.get_file_by_guest_url(args.sharing_link).download(local_file).execute_query()
    print(f"[Ok] file has been downloaded into: {download_path}")


if __name__ == "__main__":
    main()
