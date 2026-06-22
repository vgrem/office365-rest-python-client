# Microsoft Teams

Examples for working with Microsoft Teams via the Graph API —
admin, security, and management workflows.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Team.ReadBasic.All` | List teams and channels | [Teams permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `TeamMember.Read.All` | Read team members and owners | |
| `TeamSettings.Read.All` | Read team settings | |
| `Channel.ReadBasic.All` | Read channels | |
| `TeamsAppInstallation.Read.All` | Read installed apps | |
| `TeamworkTag.Read.All` | Read tags | |
| `ChannelMember.ReadWrite.All` | Manage shared channel members | |
| `Reports.Read.All` | Read usage reports | |
| `CallRecords.Read.All` | Read call quality data | |
| `OnlineMeetings.ReadWrite.All` | Create online meetings | |
| `Directory.Read.All` | List deleted teams | |

---

## Audit & Governance

| Scenario | File | Why it's useful |
|---|---|---|
| **Tenant-wide team audit** | [`audit_teams_overview.py`](./audit_teams_overview.py) | Owners, member counts, visibility, guests, archive status |
| **Settings compliance** | [`audit_team_settings.py`](./audit_team_settings.py) | Scan all teams against a policy baseline |
| **Guest access audit** | [`audit_guest_access.py`](./audit_guest_access.py) | Find teams with external guest users |
| **Lifecycle report** | [`audit_lifecycle.py`](./audit_lifecycle.py) | Archived and recently deleted teams |
| **Orphaned teams** | [`audit_orphan_owners.py`](./audit_orphan_owners.py) | Find teams without any owners |
| **Archive candidates** | [`archive_lifecycle.py`](./archive_lifecycle.py) | Find inactive teams based on last message date |
| **Inactive channels** | [`find_inactive_channels.py`](./find_inactive_channels.py) | Channels with no new messages in 90 days |

## Apps & Tags

| Scenario | File | Why it's useful |
|---|---|---|
| **App inventory** | [`apps/report.py`](./apps/report.py) | Installed apps across all teams |
| **Tag inventory** | [`tags/report.py`](./tags/report.py) | All tags with member count, untagged teams |

## Collaboration

| Scenario | File | Why it's useful |
|---|---|---|
| **Shared channel** | [`channels/shared.py`](./channels/shared.py) | Create, share, and manage access |
| **Empty/stale teams** | [`find_empty_teams.py`](./find_empty_teams.py) | Teams with no channels or no messages — cleanup candidates |
| **Excessive owners** | [`find_excessive_admins.py`](./find_excessive_admins.py) | Teams with too many owners (security risk) |
| **Export membership** | [`export_membership.py`](./export_membership.py) | All team memberships to CSV |

## Collaboration

| Scenario | File | Why it's useful |
|---|---|---|
| **Shared channel** | [`channels/shared.py`](./channels/shared.py) | Create, share, and manage access |
| **Online meetings** | [`online_meetings.py`](./online_meetings.py) | Create meetings with lobby, chat, transcription settings |

## Reports & Analytics

| Scenario | File | Why it's useful |
|---|---|---|
| **Usage report** | [`reports/usage.py`](./reports/usage.py) | Team counts and user activity over D7/D30/D90 |
| **Call records** | [`call_records.py`](./call_records.py) | Call quality analytics with sessions and segments |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

teams = client.teams.get_all().execute_query()
for t in teams:
    print(f"{t.display_name}  ({t.visibility})")
```

---

## Official docs

- [Microsoft Teams API overview](https://learn.microsoft.com/en-us/graph/api/resources/team)
- [Channels overview](https://learn.microsoft.com/en-us/graph/api/resources/channel)
- [Chat messages overview](https://learn.microsoft.com/en-us/graph/api/resources/chatmessage)
- [Teams permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions)
