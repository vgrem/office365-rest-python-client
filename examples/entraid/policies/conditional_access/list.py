"""
List Conditional Access policies, with an optional state summary.

Requires delegated permission ``Policy.Read.All``.

https://learn.microsoft.com/en-us/graph/api/conditionalaccesspolicy-list
"""

import argparse
from collections import Counter

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List Conditional Access policies")
    parser.add_argument("--summary", action="store_true", help="Show a state summary (enabled / disabled / report-only)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policies = client.policies.conditional_access_policies.get().execute_query()

    print(f"Conditional Access policies ({len(policies)}):")
    for p in policies:
        props = p.properties
        print(
            f"  {props.get('displayName', '(unnamed)'):50s}  [{props.get('state', 'disabled')}]"
            f"  created: {p.created_datetime or '?'}"
        )

    if args.summary:
        counts = Counter(p.properties.get("state", "unknown") for p in policies)
        print("\nSummary:")
        for state, count in sorted(counts.items()):
            print(f"  {state:15s} {count}")


if __name__ == "__main__":
    main()
