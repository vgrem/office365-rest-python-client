"""
Report: list all tags across all teams with member count and emails.

Shows which teams use tags, how many members each tag has, and helps
identify untagged teams or stale tags with no assigned members.

Requires application permission ``TeamworkTag.Read.All``,
``Team.ReadBasic.All``, and ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/teamworktag-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def get_tag_report() -> list[dict]:
    """Build a cross-tenant tag report."""
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    report = []

    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
        .select(["id", "displayName"])
        .top(999)
        .execute_query()
    )

    for group in groups:
        team = client.teams[group.id].get().execute_query()
        tags = team.tags.get().execute_query()

        for tag in tags:
            members = tag.members.get().execute_query()
            member_emails = []
            for m in members:
                # Members expose displayName; email not always available
                member_emails.append(m.properties.get("displayName", m.id))

            report.append(
                {
                    "team": group.display_name,
                    "tag": tag.display_name,
                    "description": getattr(tag, "description", ""),
                    "member_count": len(members),
                    "members": member_emails,
                }
            )

    return report


def main():
    print("Scanning tags across the tenant...\n")
    report = get_tag_report()

    if not report:
        print("No tags found in any team.")
        return

    print(f"Found {len(report)} tags across {len(set(r['team'] for r in report))} teams\n")

    for r in sorted(report, key=lambda x: (x["team"].lower(), x["tag"].lower())):
        emails = ", ".join(r["members"][:3])
        if len(r["members"]) > 3:
            emails += f" … +{len(r['members']) - 3}"
        print(f"Team: {r['team']}")
        print(f"  Tag: {r['tag']}  ({r['member_count']} members)")
        print(f"  Members: {emails}")
        print()

    # Identify untagged teams
    tagged_teams = {r["team"] for r in report}
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
        .select(["displayName"])
        .top(999)
        .execute_query()
    )

    untagged = [g.display_name for g in groups if g.display_name not in tagged_teams]
    if untagged:
        print(f"\nTeams without any tags ({len(untagged)}):")
        for name in untagged[:10]:
            print(f"  {name}")
        if len(untagged) > 10:
            print(f"  … and {len(untagged) - 10} more")


if __name__ == "__main__":
    main()
