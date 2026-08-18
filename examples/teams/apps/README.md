# Microsoft Teams Apps

Examples for working with Teams apps via the Graph API — catalog
inventory, app adoption, app lifecycle management, and tabs.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `AppCatalog.Read.All` | List the tenant app catalog | [App catalog permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsapp-permissions) |
| `AppCatalog.ReadWrite.All` | Install / uninstall apps in teams | |
| `Team.ReadBasic.All` | List teams and channels | [Teams permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `TeamsAppInstallation.Read.All` | Read installed apps per team | |
| `TeamsAppInstallation.ReadWrite.All` | Install / uninstall app installations | |
| `Channel.ReadBasic.All` | List channels (tabs report) | |
| `Tab.Read.All` | Read tabs | |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| App catalog inventory | [`catalog.py`](./catalog.py) | `AppCatalog.Read.All` |
| App adoption across teams | [`installed_apps.py`](./installed_apps.py) | `Team.ReadBasic.All`, `TeamsAppInstallation.Read.All` |
| Install / uninstall / inspect apps | [`manage.py`](./manage.py) | `AppCatalog.ReadWrite.All`, `TeamsAppInstallation.ReadWrite.All` |
| Tabs (pinned apps) report | [`tabs.py`](./tabs.py) | `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `Tab.Read.All` |

---

## Usage

Run from the repo root. Auth is app-only via the credentials in `tests/settings.py`.

```bash
# Catalog inventory (store / organization / sideloaded apps and versions)
python examples/teams/apps/catalog.py [--name "Planner"] [--top 100]

# Which apps are installed where, and which catalog apps are unused
python examples/teams/apps/installed_apps.py [--team <team_id>] [--catalog]

# App lifecycle in a team
python examples/teams/apps/manage.py search "Planner"
python examples/teams/apps/manage.py list --team <team_id>
python examples/teams/apps/manage.py install --team <team_id> --app <catalog_app_id>
python examples/teams/apps/manage.py uninstall --team <team_id> --installation-id <installation_id>

# Pinned apps (tabs) across teams
python examples/teams/apps/tabs.py [--team <team_id>] [--max-teams 50]
```

---

## Official docs

- [Teams app catalog API](https://learn.microsoft.com/en-us/graph/api/resources/teamsapp)
- [App installation API](https://learn.microsoft.com/en-us/graph/api/resources/teamsappinstallation)
- [Tabs API](https://learn.microsoft.com/en-us/graph/api/resources/teamstab)
