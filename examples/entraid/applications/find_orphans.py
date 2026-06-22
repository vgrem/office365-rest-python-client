"""
Find application registrations and service principals without owners.

Required delegated permissions: Application.Read.All,
ServicePrincipal.Read.All, User.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    apps = (
        client.applications.filter("owners/$count eq 0")
        .select(["displayName", "createdDateTime"])
        .consistency_level("eventual")
        .get()
        .execute_query()
    )

    sps = (
        client.service_principals.filter("owners/$count eq 0")
        .select(["displayName"])
        .consistency_level("eventual")
        .get()
        .execute_query()
    )

    total = len(apps) + len(sps)
    if apps:
        for a in apps:
            print(f"  {a.display_name}  ({a.created_date_time.date()})")
    if sps:
        print()
        for s in sps:
            print(f"  {s.display_name}")
    print(f"\nTotal orphaned: {total}")


if __name__ == "__main__":
    main()
