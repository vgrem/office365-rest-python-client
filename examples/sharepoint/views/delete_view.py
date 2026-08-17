"""
Delete a view from a list or library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Delete a view")
    parser.add_argument("--view", required=True, help="View title")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    view = ctx.web.lists.get_by_title(args.list_title).views.get_by_title(args.view)
    view.delete_object().execute_query()
    print(f"View deleted: {args.view}")


if __name__ == "__main__":
    main()
