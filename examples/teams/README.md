# Microsoft Teams

Examples for working with Microsoft Teams via the Graph API —
one basic scenario plus real-world admin, security, and management
patterns.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Team.Create` (delegated) | Create new teams | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `Group.ReadWrite.All` (delegated) | Create teams and channels from groups | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#group-permissions) |
| `TeamMember.ReadWrite.All` (delegated/application) | Add and remove team members | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `TeamsAppInstallation.ReadWriteForTeam.All` (delegated) | Install apps in a team | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `Chat.ReadWrite` (delegated) | Create and message in chats | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `TeamSettings.ReadWrite.All` (application) | Audit and remediate team settings | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `Directory.Read.All` (application) | Enumerate tenant-wide groups and deleted items | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#directory-permissions) |
| `TeamworkTag.ReadWrite.All` (delegated) | Create and manage tags | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `ChannelMember.ReadWrite.All` (delegated/application) | Manage shared channel members | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `TeamworkTag.Read.All` (application) | Read tags across all teams | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `ChannelMessage.Send` (delegated) | Send messages in channels | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |

Admin consent is required for all permissions above.

---

## Basic usage

| Scenario | File | Permission | API reference |
|---|---|---|---|
| Create a team (async, auto-waits) | [`create_team.py`](./create_team.py) | `Team.Create` | [create team](https://learn.microsoft.com/en-us/graph/api/team-post) |
| Send a message to a channel | [`channels/send_message.py`](./channels/send_message.py) | `ChannelMessage.Send` | [send message](https://learn.microsoft.com/en-us/graph/api/channel-post-messages) |
| Create a 1-on-1 chat and send a message | [`chats/create_and_message.py`](./chats/create_and_message.py) | `Chat.ReadWrite` | [create chat](https://learn.microsoft.com/en-us/graph/api/chat-post) |
| Install a Teams app | [`apps/install.py`](./apps/install.py) | `TeamsAppInstallation.ReadWriteForTeam.All` | [install app](https://learn.microsoft.com/en-us/graph/api/team-post-installedapps) |

---

## Admin & management patterns

| Scenario | File | Why it's useful |
|---|---|---|
| **Tenant-wide team audit** | [`audit_teams_overview.py`](./audit_teams_overview.py) | Owners, member counts, visibility, archive status, guests |
| **Settings governance** | [`audit_team_settings.py`](./audit_team_settings.py) | Scan all teams against a policy baseline |
| **Lifecycle report** | [`audit_lifecycle.py`](./audit_lifecycle.py) | Active, archived, and recently deleted teams |
| **Orphaned teams** | [`audit_orphan_owners.py`](./audit_orphan_owners.py) | Find teams without any owners |
| **Guest access audit** | [`audit_guest_access.py`](./audit_guest_access.py) | Find teams with external guest users |
| **Guest list** | [`guests/lifecycle.py`](./guests/lifecycle.py) | List guest users in the tenant |
| **Archive candidates** | [`archive_lifecycle.py`](./archive_lifecycle.py) | Find inactive teams based on last message |
| **Inactive channels** | [`find_inactive_channels.py`](./find_inactive_channels.py) | Channels with no recent messages |
| **Usage report** | [`reports/usage.py`](./reports/usage.py) | Team counts and user activity over D7/D30/D90 |
| **Call records** | [`call_records.py`](./call_records.py) | Call quality analytics across the tenant |
| **Online meetings** | [`online_meetings.py`](./online_meetings.py) | Create meetings with lobby and chat settings |

---

## Team lifecycle

| Scenario | File | Why it's useful |
|---|---|---|
| Create a team (async, auto-waits) | [`create_team.py`](./create_team.py) | Provision a new team |
| Create from a Microsoft 365 group | [`create_from_group.py`](./create_from_group.py) | Async with retry callback |
| Clone a team | [`clone_team.py`](./clone_team.py) | Copy channels, apps, tabs, settings, or members |
| Add a member | [`members/add.py`](./members/add.py) | Add member by email with role |
| Remove a member | [`members/remove.py`](./members/remove.py) | Remove member by email |
| Provision channels from template | [`channels/provision.py`](./channels/provision.py) | Batch create channels, skip existing |
| Shared channel | [`channels/shared.py`](./channels/shared.py) | Cross-team collaboration |
| Send message to channel | [`channels/send_message.py`](./channels/send_message.py) | Post a message in a channel |

---

## Apps & Tags

| Scenario | File | Why it's useful |
|---|---|---|
| **App inventory** | [`apps/report.py`](./apps/report.py) | Installed apps across all teams |
| Install an app | [`apps/install.py`](./apps/install.py) | Install from catalog |
| **Tag inventory** | [`tags/report.py`](./tags/report.py) | All tags with member count |
| Create a tag | [`tags/create_and_assign.py`](./tags/create_and_assign.py) | Create a tag and assign members |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

teams = client.teams.get_all().execute_query()
for t in teams:
    print(f"{t.display_name}  ({t.web_url})")
```

---

## Official docs

- [Microsoft Teams API overview](https://learn.microsoft.com/en-us/graph/api/resources/team)
- [Channels overview](https://learn.microsoft.com/en-us/graph/api/resources/channel)
- [Chat messages overview](https://learn.microsoft.com/en-us/graph/api/resources/chatmessage)
- [Chat overview](https://learn.microsoft.com/en-us/graph/api/resources/chat)
- [List all teams](https://learn.microsoft.com/en-us/graph/teams-list-all-teams)
- [Deleted items](https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-list)
- [Teams permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions)
