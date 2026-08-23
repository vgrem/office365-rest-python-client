"""
Audit external sharing across all sites — find sites shared with
users outside the organization.

Checks each site's permissions for guest users whose email domain
differs from the tenant domain.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/site-list-permissions
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Audit external sharing across sites")
    parser.add_argument("--max-sites", type=int, default=10, help="maximum number of sites to check")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Sites.Read.All")
    )

    tenant_domain = tenant.split("@")[-1] if "@" in tenant else tenant

    sites = client.sites.top(args.max_sites).get().execute_query()
    print(f"Checking {len(sites)} sites for external sharing...\n")
    found = False
    for s in sites:
        perms = s.permissions.get().execute_query()
        for p in perms:
            for identity in p.granted_to_identities:
                user = identity.user
                if not user or not user.id:
                    continue
                # Permission identities carry no email — resolve the user to inspect their domain
                user_obj = client.users[user.id].get().execute_query()
                mail = user_obj.mail or ""
                if tenant_domain not in mail:
                    print(f"  {s.display_name:45s}  {user_obj.display_name or '?':25s}  {mail or '?'}")
                    found = True
                    break

    if not found:
        print("No external sharing detected.")


if __name__ == "__main__":
    main()
