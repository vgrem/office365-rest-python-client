"""
List conditional access policies.

Conditional access policies are custom rules that define an access scenario —
who is allowed, under which conditions, and what access is granted or blocked.

https://learn.microsoft.com/en-us/graph/api/conditionalaccessroot-list-policies

Requires delegated permission ``Policy.Read.All``.
"""

import argparse
from datetime import datetime

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List conditional access policies")
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policies = client.identity.conditional_access.policies.get().execute_query()

    print(f"Conditional access policies ({len(policies)}):")
    for policy in policies:
        name = policy.get_property("displayName") or "?"
        state = policy.get_property("state") or "?"
        created = policy.created_datetime
        created_str = created.strftime("%Y-%m-%d") if created != datetime.min else "?"
        print(f"  {name:50s}  state: {state:10s}  created: {created_str}")


if __name__ == "__main__":
    main()
