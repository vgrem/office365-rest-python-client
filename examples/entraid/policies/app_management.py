"""
List app management policies and the default app management policy.

These policies enforce restrictions on app credentials (app secrets,
certificate lifetimes) — a key part of app security posture.

Requires delegated permission ``Policy.Read.ApplicationConfiguration``.

https://learn.microsoft.com/en-us/graph/api/policy-list-appmanagementpolicies
https://learn.microsoft.com/en-us/graph/api/policy-get-tenantappmanagementpolicy
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    policies = client.policies.app_management_policies.get().execute_query()
    print(f"App management policies ({len(policies)}):\n")
    for p in policies:
        props = p.properties
        print(f"  {props.get('displayName', '(unnamed)'):45s}  {props.get('description', '')}")

    default_policy = client.policies.default_app_management_policy.get().execute_query()
    print("\nDefault app management policy restrictions:")
    print(f"  {default_policy.properties}")


if __name__ == "__main__":
    main()
