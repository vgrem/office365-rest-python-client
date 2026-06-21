"""
Scan team settings across the tenant for policy compliance.

Checks guest, messaging, member, and fun settings against a
desired baseline. Requires application permissions
TeamSettings.Read.All and Directory.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

BASELINE = {
    "guestSettings": {"allowCreateUpdateChannels": False, "allowDeleteChannels": False},
    "memberSettings": {"allowCreateUpdateChannels": True, "allowDeleteChannels": True},
    "messagingSettings": {"allowUserEditMessages": True, "allowUserDeleteMessages": True, "allowUserChat": True},
    "funSettings": {"allowGiphy": False, "allowStickersAndMemes": True},
}

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

teams = client.teams.get_all().select(["id", "displayName"]).execute_query()
print(f"Scanning {len(teams)} teams...\n")

violations = 0
for team in teams:
    diffs = []
    for section, expected in BASELINE.items():
        current = team.get_property(section) or {}
        for key, val in expected.items():
            if current.get(key) != val:
                diffs.append(f"{section}.{key}: {current.get(key)} -> {val}")

    if diffs:
        violations += 1
        print(f"  {team.display_name}:  {'; '.join(diffs)}")

if violations:
    print(f"\n{violations}/{len(teams)} teams deviate from baseline.")
else:
    print("All teams comply with the policy baseline.")
