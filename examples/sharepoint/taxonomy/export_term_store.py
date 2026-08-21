"""
Exports the term store groups and term sets to JSON.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    argparse.ArgumentParser(description="Export term store groups and term sets to JSON").parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

    term_groups = ctx.taxonomy.term_store.term_groups.get().execute_query()
    for term_group in term_groups:
        term_group.term_sets.get().execute_query()
    print(json.dumps(term_groups.to_json(), indent=4))


if __name__ == "__main__":
    main()
