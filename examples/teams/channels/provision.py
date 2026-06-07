"""
Provision multiple channels in a team from a declarative template.

Channels are created sequentially — each depends on the previous
``execute_query`` to complete.  This pattern is useful when you need
to bootstrap a new team with a standard channel structure.

Requires delegated permission ``Channel.Create`` or
``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/channel-post
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

# — Channel template —
CHANNEL_TEMPLATE = [
    {"displayName": "General", "description": "Company-wide announcements and Q&A"},
    {"displayName": "Engineering", "description": "Sprints, PRs, and technical discussions"},
    {"displayName": "Design", "description": "UX reviews, mockups, and design system"},
    {"displayName": "Product", "description": "Roadmap, requirements, and feedback"},
    {"displayName": "Random", "description": "Water-cooler chat and non-work banter"},
]

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

my_teams = client.me.joined_teams.get().top(1).execute_query()
if len(my_teams) == 0:
    sys.exit("No teams found")

team = my_teams[0]
print(f"Provisioning channels in '{team.display_name}'...\n")

provisioned = 0
for spec in CHANNEL_TEMPLATE:
    # Skip if channel already exists
    existing = team.channels.get().filter(f"displayName eq '{spec['displayName']}'").execute_query()
    if len(existing) > 0:
        print(f"  ↻ {spec['displayName']} — already exists, skipped")
        continue

    channel = team.channels.add(
        display_name=spec["displayName"],
        description=spec["description"],
    ).execute_query()
    print(f"  ✓ {spec['displayName']} — created (id: {channel.id})")
    provisioned += 1

print(f"\nDone. {provisioned} channels created.")
