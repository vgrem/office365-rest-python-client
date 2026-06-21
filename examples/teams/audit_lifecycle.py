"""
Lifecycle: report on archived and recently deleted teams.

Archived teams remain in the directory but are read-only.
Deleted teams are soft-deleted and restorable for 30 days.

Requires application permission ``Team.ReadBasic.All``,
``Directory.Read.All``, and ``Group.Read.All``.

https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-list
https://learn.microsoft.com/en-us/graph/api/team-archive
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

teams = client.teams.get_all().select(["id", "displayName", "deletedDateTime"]).execute_query()
archived = [t for t in teams if t.is_archived]
active = [t for t in teams if not t.is_archived]

print(f"Active teams : {len(active)}")
print(f"Archived     : {len(archived)}\n")
for g in archived:
    print(f"  {g.display_name}")

deleted_teams = client.directory.deleted_teams.get().select(["id", "displayName", "deletedDateTime"]).execute_query()
print(f"\nRecently deleted (restorable): {len(deleted_teams)}")
for del_team in deleted_teams:
    label = ""
    if del_team.deleted_datetime:
        deleted_dt = del_team.deleted_datetime.replace(tzinfo=timezone.utc)
        days_ago = (datetime.now(timezone.utc) - deleted_dt).days
        remaining = max(0, 30 - days_ago)
        label = f" (deleted {days_ago}d ago, {remaining}d to restore)"
    print(f"  {del_team.get_property('displayName')}{label}")
