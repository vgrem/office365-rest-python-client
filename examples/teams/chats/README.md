# Microsoft Teams Chats

Examples for working with Teams chats via the Graph API — inventory,
lifecycle, and messaging.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Chat.Read` (delegated) / `Chat.Read.All` | List chats and messages | [Chat permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#chat-permissions) |
| `Chat.ReadWrite` (delegated) / `Chat.ReadWrite.All` | Send messages, manage members | |
| `Chat.Create` | Create chats | |

Chats are user-scoped: use `--me` for the signed-in user (delegated) or
`--user <id|UPN>` / `--user1/--user2` for app-only.

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| Chat inventory | [`inventory.py`](./inventory.py) | `Chat.Read` / `Chat.Read.All` |
| Chat lifecycle | [`manage.py`](./manage.py) | `Chat.Create`, `Chat.ReadWrite` |
| Messaging & activity | [`messages.py`](./messages.py) | `Chat.ReadWrite`, `Chat.Read` |

---

## Usage

Run from the repo root. Auth via the credentials in `tests/settings.py`.

```bash
# Inventory a user's chats (delegated or app-only)
python examples/teams/chats/inventory.py --me
python examples/teams/chats/inventory.py --user meganb@contoso.com [--top 50]

# Lifecycle
python examples/teams/chats/manage.py create-one-on-one --user1 <id|UPN> --user2 <id|UPN>
python examples/teams/chats/manage.py create-group --members <id> <id> [<id> ...] [--topic "Project"]
python examples/teams/chats/manage.py members --chat <chat_id>
python examples/teams/chats/manage.py add-member --chat <chat_id> --user <id|UPN> [--role owner]
python examples/teams/chats/manage.py delete --chat <chat_id>

# Messaging
python examples/teams/chats/messages.py send --chat <chat_id> --content "Hello"
python examples/teams/chats/messages.py reply --chat <chat_id> --message <msg_id> --content "Hi back"
python examples/teams/chats/messages.py list --chat <chat_id> [--top 10]
python examples/teams/chats/messages.py export --chat <chat_id> [--output chat.jsonl]
python examples/teams/chats/messages.py digest --me [--top 20]
```

---

## Official docs

- [Chat resource](https://learn.microsoft.com/en-us/graph/api/resources/chat)
- [Chat message resource](https://learn.microsoft.com/en-us/graph/api/resources/chatmessage)
- [Chat permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#chat-permissions)
