"""
Governance: scan team settings across the entire tenant and identify
policy violations.

Checks guest, messaging, member, and fun settings on every team and
reports teams that deviate from the desired baseline.

Requires application permission ``TeamSettings.Read.All``,
``TeamSettings.ReadWrite.All``, and ``Directory.Read.All``.

https://learn.microsoft.com/en-us/graph/api/team-update
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

# — Desired baseline —
BASELINE = {
    "guestSettings": {"allowCreateUpdateChannels": False, "allowDeleteChannels": False},
    "memberSettings": {"allowCreateUpdateChannels": True, "allowDeleteChannels": True},
    "messagingSettings": {"allowUserEditMessages": True, "allowUserDeleteMessages": True, "allowUserChat": True},
    "funSettings": {"allowGiphy": False, "allowStickersAndMemes": True},
}

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

groups = (
    client.groups.get()
    .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
    .select(["id", "displayName"])
    .top(999)
    .execute_query()
)

print(f"Scanning {len(groups)} teams against policy baseline...\n")

violations = 0

for group in groups:
    team = client.teams[group.id].get().execute_query()

    diffs = []
    for section, expected in BASELINE.items():
        current = team.get_property(section) or {}
        for key, val in expected.items():
            if current.get(key) != val:
                diffs.append(f"  {section}.{key}: {current.get(key)} → {val}")

    if diffs:
        violations += 1
        print(f"  ⚠ {group.display_name}")
        for d in diffs:
            print(d)
        print()

if violations == 0:
    print("✅ All teams comply with the policy baseline.\n")
else:
    total = len(groups)
    print(f"Summary: {violations}/{total} teams deviate from baseline.\n")

    # Uncomment to auto-remediate:
    # for group in groups:
    #     team = client.teams[group.id].get().execute_query()
    #     for section, settings in BASELINE.items():
    #         team.set_property(section, settings)
    #     team.update().execute_query()
    # print(f"Remediated {violations} teams to baseline.")
