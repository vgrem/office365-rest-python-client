"""
Group inventory — every group with its type and mail address.

Requires application permission ``Group.Read.All``.

https://learn.microsoft.com/en-us/graph/api/group-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    groups = client.groups.get_all().execute_query()

    counts: dict[str, int] = {}
    for group in groups:
        if group.group_types:
            kind = "Microsoft 365"
        elif group.mail_enabled:
            kind = "Distribution"
        else:
            kind = "Security"
        counts[kind] = counts.get(kind, 0) + 1
        print(f"{group.display_name:45s}  {kind:15s}  {group.mail or '-'}")

    summary = ", ".join(f"{kind}: {count}" for kind, count in sorted(counts.items()))
    print(f"\nTotal {len(groups)} group(s) — {summary}")


if __name__ == "__main__":
    main()
