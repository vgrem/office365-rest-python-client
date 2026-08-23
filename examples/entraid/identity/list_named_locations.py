"""
List conditional access named locations.

Named locations define trusted network locations (IP ranges or countries/regions)
that conditional access policies can reference in grant/block conditions.

https://learn.microsoft.com/en-us/graph/api/conditionalaccessroot-list-namedlocations

Requires delegated permission ``Policy.Read.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List conditional access named locations")
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    locations = client.identity.conditional_access.named_locations.get().execute_query()

    print(f"Named locations ({len(locations)}):")
    for loc in locations:
        name = loc.get_property("displayName") or "?"
        loc_type = type(loc).__name__
        trusted = loc.get_property("isTrusted")
        detail = f"  trusted: {trusted}" if trusted is not None else ""
        print(f"  {loc_type:<25s}  {name}{detail}")


if __name__ == "__main__":
    main()
