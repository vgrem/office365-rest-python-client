# Microsoft Teams Channels

Examples for working with Teams channels via the Graph API — inventory,
lifecycle management, messaging, and shared channels.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Team.ReadBasic.All` | List teams and channels | [Teams permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#teams-permissions) |
| `Channel.ReadBasic.All` | Read channels | |
| `Channel.Create` | Create channels | |
| `ChannelSettings.ReadWrite.All` | Update channels, provision email | |
| `Channel.Delete.All` | Delete channels | |
| `ChannelMessage.Read.All` | Read channel messages | |
| `ChannelMessage.Send` | Send and reply to messages | |
| `ChannelMember.ReadWrite.All` | Manage (shared) channel members | |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| Cross-team channel inventory | [`inventory.py`](./inventory.py) | `Team.ReadBasic.All`, `Channel.ReadBasic.All` |
| Channel lifecycle | [`manage.py`](./manage.py) | `Channel.Create`, `ChannelSettings.ReadWrite.All`, `Channel.Delete.All` |
| Messaging & activity digest | [`messages.py`](./messages.py) | `ChannelMessage.Read.All`, `ChannelMessage.Send` |
| Shared channels | [`shared.py`](./shared.py) | `Channel.Create`, `ChannelMember.ReadWrite.All` |

---

## Usage

Run from the repo root. Auth is app-only via the credentials in `tests/settings.py`.

```bash
# Inventory / audit
python examples/teams/channels/inventory.py [--team <team_id>] [--max-teams 50]

# Lifecycle
python examples/teams/channels/manage.py list --team <team_id>
python examples/teams/channels/manage.py create --team <team_id> --name "Announcements" [--type private] [--description "..."]
python examples/teams/channels/manage.py update --team <team_id> --channel <channel_id> [--name ...] [--description ...]
python examples/teams/channels/manage.py delete --team <team_id> --channel <channel_id>
python examples/teams/channels/manage.py provision-email --team <team_id> --channel <channel_id>
python examples/teams/channels/manage.py remove-email --team <team_id> --channel <channel_id>
python examples/teams/channels/manage.py primary --team <team_id>

# Messaging
python examples/teams/channels/messages.py send --team <team_id> --channel <channel_id> --content "Hello"
python examples/teams/channels/messages.py reply --team <team_id> --channel <channel_id> --message <msg_id> --content "Hi back"
python examples/teams/channels/messages.py list --team <team_id> --channel <channel_id> [--top 10]
python examples/teams/channels/messages.py digest --team <team_id>

# Shared channels
python examples/teams/channels/shared.py create --host-name "Marketing" --guest-name "Engineering" --name "Project Alpha" [--member meganb@contoso.com]
python examples/teams/channels/shared.py list --team-name "Marketing" --channel <channel_id>
python examples/teams/channels/shared.py has-access --team-name "Marketing" --channel <channel_id> --user meganb@contoso.com
```

---

## Official docs

- [Channel overview](https://learn.microsoft.com/en-us/graph/api/resources/channel)
- [Shared channels](https://learn.microsoft.com/en-us/graph/api/resources/sharedwithchannelteaminfo)
- [Channel messages](https://learn.microsoft.com/en-us/graph/api/resources/chatmessage)
