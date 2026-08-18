"""
Create a Conditional Access policy (dry-run by default).

Builds a policy body (applications, conditions, grantControls, state) and
submits it. Use ``--commit`` to actually create it.

Requires delegated permission ``Policy.ReadWrite.ConditionalAccess``.

https://learn.microsoft.com/en-us/graph/api/conditionalaccesspolicy-post
"""

import argparse
import json

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a Conditional Access policy")
    parser.add_argument("--name", default="Block legacy authentication", help="Policy display name")
    parser.add_argument("--commit", action="store_true", help="Actually create the policy (default: dry-run)")
    args = parser.parse_args()

    policy_body = {
        "displayName": args.name,
        "state": "enabled",
        "conditions": {
            "clientAppTypes": ["other", "mobileAppsAndDesktopClients"],
            "applications": {"includeApplications": ["all"]},
            "users": {"includeUsers": ["all"]},
        },
        "grantControls": {"operator": "OR", "builtInControls": ["block"]},
    }

    if not args.commit:
        print(f"[dry-run] would create policy '{args.name}':")
        print(json.dumps(policy_body, indent=2))
        return

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policy = client.identity.conditional_access.policies.add(**policy_body).execute_query()
    print(f"Created policy: {policy.properties.get('displayName')}  (id: {policy.id})")


if __name__ == "__main__":
    main()
