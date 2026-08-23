"""
List the identity providers configured for a tenant.

Also lists the identity provider types that Microsoft Entra ID supports.

https://learn.microsoft.com/en-us/graph/api/identitycontainer-list-identityproviders
https://learn.microsoft.com/en-us/graph/api/identityproviderbase-availableprovidertypes

Requires delegated permission ``IdentityProvider.Read.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List configured identity providers")
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    providers = client.identity.identity_providers.get().execute_query()
    print(f"Configured identity providers ({len(providers)}):")
    for idp in providers:
        name = idp.display_name or "?"
        provider_type = (
            idp.get_property("identityProviderType") or idp.get_property("providerType") or type(idp).__name__
        )
        print(f"  {name:40s}  {provider_type}")

    available = client.identity.identity_providers.available_provider_types().execute_query().value
    print(f"\nSupported provider types ({len(available)}):")
    print(f"  {', '.join(str(t) for t in available)}")


if __name__ == "__main__":
    main()
