"""
Exports list view items to a CSV file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Export view items to CSV")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--view", default="All Documents", help="View title")
    parser.add_argument("--output", help="Output CSV path (default: temp file)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    list_view = ctx.web.lists.get_by_title(args.list_title).views.get_by_title(args.view)
    export_path = args.output or os.path.join(tempfile.mkdtemp(), f"{args.view}.csv")

    with open(export_path, "w", newline="", encoding="utf-8") as f:
        list_view.get_items().to_csv(f).execute_query()

    print(f"List view has been exported into '{export_path}' file")


if __name__ == "__main__":
    main()
