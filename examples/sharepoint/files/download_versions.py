"""
Demonstrates how to download file versions from a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def download_all_versions(remote_file, target_dir: str):
    versions = remote_file.versions.get().execute_query()
    for version in versions:
        local_path = os.path.join(target_dir, f"{version.version_label}_{remote_file.name}")
        with open(local_path, "wb") as f:
            version.download(f).execute_query()
        print(f"  {version.version_label}: downloaded -> {local_path}")


def download_specific_version(remote_file, version_id: int, target_path: str):
    version = remote_file.versions.get_by_id(version_id)
    with open(target_path, "wb") as f:
        version.download(f).execute_query()
    print(f"  version {version.version_label} downloaded -> {target_path}")


def main():
    parser = argparse.ArgumentParser(description="Download file versions")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    parser.add_argument("--version-id", type=int, default=None, help="download only this version id")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    remote_file = ctx.web.get_file_by_server_relative_path(args.file_url)
    target_dir = tempfile.mkdtemp()

    if args.version_id is not None:
        download_specific_version(remote_file, args.version_id, os.path.join(target_dir, "version.bin"))
    else:
        download_all_versions(remote_file, target_dir)


if __name__ == "__main__":
    main()
