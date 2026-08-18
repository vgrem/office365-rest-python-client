"""
List authentication strength policies — including phishing-resistant MFA.

Requires delegated permission ``Policy.Read.All``.

https://learn.microsoft.com/en-us/graph/api/authenticationstrengthpolicy-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policies = client.policies.authentication_strength_policies.get().execute_query()

    print(f"Authentication strength policies ({len(policies)}):\n")
    for p in policies:
        props = p.properties
        print(f"  {props.get('displayName', '(unnamed)'):45s}  [{props.get('policyType', '?')}]")


if __name__ == "__main__":
    main()
