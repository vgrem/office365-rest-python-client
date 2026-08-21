"""
Gets a term group by name from the term store.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Get a term group by name from the term store")
    parser.add_argument("--group-name", default="Geography", help="term group name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
    term_group = ctx.taxonomy.term_store.term_groups.get_by_name(args.group_name).execute_query()
    print(term_group)


if __name__ == "__main__":
    main()
