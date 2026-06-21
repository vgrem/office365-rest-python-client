# Outlook — Mail, Calendar & Events

Examples for working with Outlook mail, calendar, and events via
Microsoft Graph.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Mail.ReadWrite` (delegated) | Read, send, and manage messages | [Mail permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Mail.Send` (delegated) | Send mail on behalf of the signed-in user | [Mail permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Calendars.ReadWrite` (delegated) | Create, read, update, delete events and calendars | [Calendar permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#calendars-permissions) |
| `MailboxSettings.ReadWrite` (delegated) | Read and update automatic replies, rules | [Mail permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Mail.Read` (delegated) | Read mail tips and message properties | [Mail permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#mail-permissions) |
| `Reports.Read.All` (delegated) | Access email and mailbox usage reports | [Reports permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#reports-permissions) |
| `User.Read.All` (delegated or app) | Read user properties for mailbox audit, shared mailboxes, forwarding detection | [User permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#user-permissions) |
| `Contacts.ReadWrite` (delegated) | Create, read, update, delete personal contacts | [Contacts permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#contacts-permissions) |
| `Place.Read.All` (delegated) | List rooms and room lists | [Places permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#places-permissions) |
| `Calendars.Read` (app) | Read-only calendar access across tenants | [Calendar permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#calendars-permissions) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_username_and_password(
    "client_id", "user@contoso.com", "password"
)

# Send a quick message
client.me.send_mail(
    subject="Hello",
    body="This is a test.",
    to_recipients=["recipient@contoso.com"],
).execute_query()
```

---

## Mail — Messages & Folders

| Scenario | File | Why it's useful |
|---|---|---|
| **Send a message** | [`messages/send.py`](./messages/send.py) | Simplest send — recipient, subject, body |
| **Send with large attachment** | [`messages/send_with_large_attachment.py`](./messages/send_with_large_attachment.py) | Upload session pattern required for files >3 MB |
| **Export messages to CSV** | [`messages/export_folder_csv.py`](./messages/export_folder_csv.py) | Audit or backup — dump folder contents with subject, sender, date, size |
| **Find large messages** | [`messages/large_messages.py`](./messages/large_messages.py) | Storage management — find oversized messages by size threshold |
| **Clean up old messages** | [`messages/cleanup_old.py`](./messages/cleanup_old.py) | Retention — dry-run then delete messages older than X days |
| **Archive old messages** | [`messages/archive_old.py`](./messages/archive_old.py) | Retention — move messages older than X to Archive folder |
| **Paginate through mail** | [`messages/pagination.py`](./messages/pagination.py) | Walk thousands of messages with $top/$skip |
| **Message lifecycle** | [`messages/lifecycle.py`](./messages/lifecycle.py) | Reply, forward, move, copy in one flow |
| **Folder management** | [`messages/folders.py`](./messages/folders.py) | Create, empty, mark-all-read, permanent delete |
| **Inbox rules + categories** | [`messages/inbox_rules.py`](./messages/inbox_rules.py) | Automate message handling with rules and categories |
| **Mailbox settings (OOF)** | [`messages/mailbox_settings.py`](./messages/mailbox_settings.py) | Enable scheduled automatic replies (Out of Office) |
| **Mail tips** | [`messages/mail_tips.py`](./messages/mail_tips.py) | Pre-flight check — OOF, moderation, size limits |
| **Export MIME** | [`messages/export_mime.py`](./messages/export_mime.py) | Download message as .eml for backup or eDiscovery |
| **Email search** | [`messages/search.py`](./messages/search.py) | Microsoft Search query across mailbox |

## Mail — Administration & Reporting

| Scenario | File | Why it's useful |
|---|---|---|
| **Email usage report** | [`reports/email_usage.py`](./reports/email_usage.py) | Activity counts and mailbox storage across D7/D30/D90 |
| **Mailbox audit** | [`mailboxes/report.py`](./mailboxes/report.py) | Auto-replies and mailbox settings across users |
| **Shared mailboxes** | [`shared_mailboxes/report.py`](./shared_mailboxes/report.py) | Discover and validate shared mailbox setup |
| **Mail flow audit** | [`mail_flow/forwarding_report.py`](./mail_flow/forwarding_report.py) | Security — detect users forwarding mail externally |

## Calendar — Events

| Scenario | File | Why it's useful |
|---|---|---|
| **Create an event** | [`events/create.py`](./events/create.py) | Schedule a meeting with attendees and details |
| **Recurring event** | [`events/recurring.py`](./events/recurring.py) | Weekly, monthly patterns with limited occurrences |
| **Meeting response** | [`events/respond.py`](./events/respond.py) | Accept, decline, or cancel as organizer/attendee |
| **Find meeting times & schedule** | [`calendars/availability.py`](./calendars/availability.py) | Availability lookup and free/busy schedule |
| **Share calendar** | [`calendars/share.py`](./calendars/share.py) | Grant read access to another user |
| **Delegate calendar** | [`calendars/delegate.py`](./calendars/delegate.py) | Grant editor/delegate access to manage events |

## Calendar — Administration & Reporting

| Scenario | File | Why it's useful |
|---|---|---|
| **Export events to CSV** | [`calendars/events_export_csv.py`](./calendars/events_export_csv.py) | Audit or migration — export by date range |
| **Clean up old events** | [`calendars/events_cleanup.py`](./calendars/events_cleanup.py) | Dry-run then delete events older than N days |
| **External attendees** | [`calendars/external_attendees.py`](./calendars/external_attendees.py) | Governance — find meetings with guest attendees |
| **Calendar permissions report** | [`calendars/permissions_report.py`](./calendars/permissions_report.py) | Audit who has access and what role |
| **Copy events between calendars** | [`calendars/events_copy.py`](./calendars/events_copy.py) | Migration or reorganization |

## Contacts

| Scenario | File | Why it's useful |
|---|---|---|
| **Contact CRUD** | [`contacts/manage.py`](./contacts/manage.py) | Create, read, update, delete with contact folders |

---

## Official docs

- [Outlook mail API overview](https://learn.microsoft.com/en-us/graph/api/resources/message)
- [Outlook calendar API overview](https://learn.microsoft.com/en-us/graph/api/resources/event)
- [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
