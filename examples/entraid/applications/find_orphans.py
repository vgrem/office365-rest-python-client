"""
Find application registrations and service principals without owners.

Orphaned apps are a governance risk — no one to review permissions,
renew expiring secrets, or respond to security incidents.
This script identifies apps missing owner assignments.

Inspired by Add-OwnerstoApps.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Application.Read.All         Read app registrations
    ServicePrincipal.Read.All    Read service principals
    User.Read.All                Resolve display names

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def find_apps_without_owners() -> tuple[list[dict], list[dict]]:
    """Find apps and service principals without owners.

    Returns:
        Tuple of (apps_no_owners, sps_no_owners).
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    apps_no_owners = []
    sps_no_owners = []

    # 1. Check app registrations
    apps = client.applications.get().execute_query()
    for app in apps:
        app_name = getattr(app, "display_name", "Unnamed")
        app_id = getattr(app, "id", "")

        try:
            owners = client.applications[app_id].owners.get().execute_query()
            if not owners:
                apps_no_owners.append(
                    {
                        "name": app_name,
                        "id": app_id,
                        "created": getattr(app, "created_date_time", None),
                    }
                )
        except Exception:
            pass

    # 2. Check service principals
    sps = client.service_principals.get().execute_query()
    for sp in sps:
        sp_name = getattr(sp, "display_name", "Unnamed")
        sp_id = getattr(sp, "id", "")

        try:
            owners = client.service_principals[sp_id].owners.get().execute_query()
            if not owners:
                sps_no_owners.append(
                    {
                        "name": sp_name,
                        "id": sp_id,
                    }
                )
        except Exception:
            pass

    return apps_no_owners, sps_no_owners


def main():
    print("Finding orphaned application registrations...\n")
    apps, sps = find_apps_without_owners()

    total = len(apps) + len(sps)

    if total == 0:
        print("No orphaned applications found. ✓")
        return

    if apps:
        print(f"App registrations without owners ({len(apps)}):\n")
        for a in sorted(apps, key=lambda x: x["name"].lower()):
            created = a["created"].strftime("%Y-%m-%d") if a["created"] else "Unknown"
            print(f"  {a['name']:40s}  (created: {created})")

    if sps:
        print(f"\nService principals without owners ({len(sps)}):\n")
        for s in sorted(sps, key=lambda x: x["name"].lower())[:20]:
            print(f"  {s['name']}")
        if len(sps) > 20:
            print(f"  ... and {len(sps) - 20} more")

    print(f"\nTotal orphaned: {total} — review and assign owners.")


if __name__ == "__main__":
    main()
