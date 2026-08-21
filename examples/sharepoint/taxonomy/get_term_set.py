"""
Finds term sets by name within a term group.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Find term sets by name within a term group")
    parser.add_argument("--group-name", default="Geography", help="term group name")
    parser.add_argument("--term-set-name", default="Countries", help="term set name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
    term_group = ctx.taxonomy.term_store.term_groups.get_by_name(args.group_name)
    term_sets = term_group.get_term_sets_by_name(args.term_set_name).execute_query()
    for ts in term_sets:
        print(ts)


if __name__ == "__main__":
    main()
