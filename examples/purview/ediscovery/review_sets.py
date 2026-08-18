"""
List review sets for an eDiscovery case.

Requires delegated permission ``eDiscovery.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-ediscoverycase-list-reviewsets
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List eDiscovery review sets")
    parser.add_argument("--case-id", help="eDiscovery case id (default: first case)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    cases = client.security.cases.ediscovery_cases.get().execute_query()
    if not len(cases):
        raise SystemExit("No eDiscovery cases found")

    case = next((c for c in cases if c.id == args.case_id), None) if args.case_id else cases[0]
    if case is None:
        raise SystemExit(f"eDiscovery case '{args.case_id}' not found")

    review_sets = case.review_sets.get().execute_query()
    print(f"Review sets for case '{case.properties.get('displayName')}' ({len(review_sets)}):")
    for rs in review_sets:
        props = rs.properties
        print(f"  {props.get('displayName', '(unnamed)')}  (id: {rs.id})")


if __name__ == "__main__":
    main()
