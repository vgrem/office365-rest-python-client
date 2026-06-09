"""
Export groups with members to CSV — group structure for migration
mapping and planning.

Exports all groups with their membership list, ownership, group
type, visibility, and creation date. Useful for:
  - Mapping group structure during tenant-to-tenant migration
  - Membership audit and cleanup
  - Security group review

Requires delegated permission ``Group.Read.All``,
``Directory.Read.All``.

https://learn.microsoft.com/en-us/graph/api/group-list
"""

import csv

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

OUTPUT_FILE = "/tmp/groups_export.csv"


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    print("Fetching groups...")
    groups = client.groups.get_all().execute_query()
    print(f"  Found {len(groups)} groups\n")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "groupId",
                "displayName",
                "mail",
                "groupType",
                "visibility",
                "description",
                "createdDateTime",
                "memberCount",
                "members (UPN)",
                "owners (UPN)",
            ]
        )

        for g in groups:
            gid = g.id or "?"
            display = g.display_name or "(unnamed)"
            mail = g.mail or ""
            gtype = (
                "Microsoft 365"
                if g.mail_enabled and not g.security_enabled
                else "Security"
                if g.security_enabled
                else "Distribution"
            )
            visibility = g.visibility or "?"
            desc = (g.description or "")[:80]
            created = g.created_date_time.strftime("%Y-%m-%d") if g.created_date_time else ""

            # Load members and owners
            member_upns = []
            owner_upns = []

            try:
                members = g.members.get().execute_query()
                member_upns = [m.user_principal_name for m in members if hasattr(m, "user_principal_name")][:20]
            except Exception:
                pass

            try:
                owners = g.owners.get().execute_query()
                owner_upns = [o.user_principal_name for o in owners if hasattr(o, "user_principal_name")]
            except Exception:
                pass

            writer.writerow(
                [
                    gid,
                    display,
                    mail,
                    gtype,
                    visibility,
                    desc,
                    created,
                    len(member_upns),
                    ";".join(member_upns) if member_upns else "",
                    ";".join(owner_upns) if owner_upns else "",
                ]
            )

            print(f"  {display:40s}  type={gtype:15s}  members={len(member_upns):>4}  owners={len(owner_upns)}")

    print(f"\n✓ Exported {len(groups)} groups to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
