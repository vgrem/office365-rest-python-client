"""
Audit files in a SharePoint document library for sharing links.

Scans each file's sharing information and flags files with active
sharing links — especially anonymous/external links — for security
review.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Audit files for sharing links")
    parser.add_argument("--library", default="Shared Documents", help="document library to scan")
    parser.add_argument("--max-files", type=int, default=500, help="maximum files to scan (default 500)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lib = ctx.web.lists.get_by_title(args.library)
    files = lib.root_folder.files.get_all(args.max_files).execute_query()
    if not files:
        sys.exit("No files found in the library.")

    shared = 0
    anonymous = 0
    for f in files:
        info = f.get_sharing_information().execute_query()
        links = info.sharing_links
        if not len(links):
            continue
        shared += 1
        for link in links:
            kind = "ANONYMOUS" if link.AllowsAnonymousAccess else "internal"
            if link.AllowsAnonymousAccess:
                anonymous += 1
            print(f"  [{kind:9s}] {f.name}  ->  {link.Url}")

    print(f"\nScanned {len(files)} files: {shared} with sharing links ({anonymous} anonymous/external).")


if __name__ == "__main__":
    main()
