"""Deletes all non-system lists from a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Delete all non-system lists from a site")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--dry-run", action="store_true", help="list the lists to delete without deleting")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)
    lists = ctx.web.lists.get().select(["IsSystemList", "Title", "Id"]).filter("IsSystemList eq false").execute_query()
    print(f"{len(lists)} lists found")

    for lst in lists:
        if args.dry_run:
            print(f"  would delete: {lst.title}")
        else:
            lst.delete_object()

    if not args.dry_run:
        ctx.execute_batch()
        print(f"{len(lists)} lists deleted")


if __name__ == "__main__":
    main()
