"""Deletes all non-system lists from a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url


def main():
    parser = argparse.ArgumentParser(description="Delete all non-system lists from a site")
    parser.add_argument("--dry-run", action="store_true", help="list the lists to delete without deleting")
    args = parser.parse_args()

    ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
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
