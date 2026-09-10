# Teams Migration (export)

Back up Teams through the unified `MigrationJob` adapters — team structure,
members, channels, tabs, apps, messages (with replies, inline images), and
optionally channel files. Import is planned next.

## Archive layout

```
<output>/
  <team-id>/
    team.json                        # metadata, members, channels, tabs, apps
    messages.ndjson                  # one message/reply per line
    attachments/<channel>/<msg>_<content>.<ext>
    files/<channel>.zip              # --files
```

## Commands

```bash
# One team (repeat --team for several), with files
python export_team.py --team 00000000-0000-0000-0000-000000000000 --output ./backup --files

# Every team in the tenant
python export_team.py --all --output ./backup

# Resume an interrupted run
python export_team.py --all --output ./backup --resume

# Compliance message export (deferred collection adapters)
python export_messages.py --output ./messages --team <team-id>
python export_messages.py --output ./messages --user user@contoso.com
python export_messages.py --output ./messages --tenant
python export_messages.py --output ./messages --filter "createdDateTime gt 2024-01-01T00:00:00Z"
```

## Permissions (application)

| Scenario | Permissions |
|---|---|
| Structure, members, channels, tabs, apps | `Team.ReadBasic.All`, `TeamMember.Read.All` |
| Messages | `ChannelMessage.Read.All`, `Chat.Read.All`, `Teamwork.Migrate.All` |
| Channel files (`--files`) | `Files.Read.All`, `Sites.Read.All` |

## Library usage

```python
from pathlib import Path

from office365.graph_client import GraphClient
from office365.migration import MigrationJob
from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget, TeamsExportOptions

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

job = MigrationJob(
    TeamsArchiveSource(client, ["00000000-..."], TeamsExportOptions(include_files=True)),
    TeamsArchiveTarget("./backup"),
    checkpoint_path=Path("./backup.checkpoint.json"),
)
job.plan()
stats = job.run()
print(stats.summary(), job.verify().summary())

# Messages only — deferred collection adapters
with open("messages.ndjson", "w") as f:
    client.teams.get_all_messages() \
        .filter("createdDateTime gt 2024-01-01T00:00:00Z") \
        .get_all() \
        .to_ndjson(f) \
        .download_hosted_contents("attachments") \
        .execute_query()
```
