"""Delete a SharePoint list by title (idempotently).

Re-running is safe: ``delete_object(ignore_missing=True)`` treats an already-absent
list as success instead of raising.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    p = argparse.ArgumentParser(description="Delete a SharePoint list by title")
    p.add_argument("--list-title", default="Stocks_5yr_Large")
    args = p.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ctx.web.lists.get_by_title(args.list_title).delete_object(ignore_missing=True).execute_query()
    print(f"List '{args.list_title}' has been deleted")


if __name__ == "__main__":
    main()
