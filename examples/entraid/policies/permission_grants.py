"""
List permission grant policies — the admin and user consent posture.

Requires delegated permission ``Policy.Read.PermissionGrant``.

https://learn.microsoft.com/en-us/graph/api/permissiongrantpolicy-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policies = client.policies.permission_grant_policies.get().execute_query()

    print(f"Permission grant policies ({len(policies)}):\n")
    for p in policies:
        props = p.properties
        print(f"  {props.get('displayName', '(unnamed)'):45s}  [{props.get('deletedDateTime') or 'active'}]")


if __name__ == "__main__":
    main()
