"""
List self-service sign-up (B2X) user flows.

B2X user flows enable a self-service sign-up experience for guest users,
defining which identity providers and attributes are collected during sign-up.

https://learn.microsoft.com/en-us/graph/api/identitycontainer-list-b2xuserflows

Requires delegated permission ``IdentityUserFlow.Read.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List self-service sign-up user flows")
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    flows = client.identity.b2x_user_flows.get().execute_query()

    print(f"Self-service sign-up user flows ({len(flows)}):")
    for flow in flows:
        name = flow.get_property("displayName") or "?"
        flow_type = flow.user_flow_type or "?"
        print(f"  {name:50s}  {flow_type}")


if __name__ == "__main__":
    main()
