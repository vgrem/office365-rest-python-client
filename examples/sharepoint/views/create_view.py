"""
Create a custom view on a list or library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a custom view")
    parser.add_argument("--view", required=True, help="View title")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--fields", nargs="+", default=["Title", "Modified"], help="Columns to include")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    view = target_list.views.create(title=args.view, fields=args.fields).execute_query()
    print(f"View created: {view.title}  (ID: {view.id})")


if __name__ == "__main__":
    main()
