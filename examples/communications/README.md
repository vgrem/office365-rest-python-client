# Working with cloud communications

`client.communications` is Microsoft Graph's **cloud communications** endpoint:
presence, online meetings, calls and call records. "Communications" is the API
namespace, not a product — Teams, a contact centre or a softphone all sit on top
of it.

## The model

```mermaid
flowchart LR
    C["client.communications"] --> P["presences<br/>who is reachable"]
    C --> M["online_meetings<br/>join links &amp; artifacts"]
    C --> CR["call_records<br/>call quality, Direct Routing"]
    C --> CA["calls · adhoc_calls<br/>real-time calling"]
```

Three independent areas — with three different permission stories:

| Area | Who may call it | Folder |
| --- | --- | --- |
| Presence | a user's own presence (delegated) | [`presence/`](./presence/) |
| Online meetings | the signed-in organizer's meetings (delegated) | [`meetings/`](./meetings/) |
| Call records | **application only** — no "my calls" version | [`callrecords/`](./callrecords/) |

Real-time `calls` and `adhoc_calls` need a media bot (application- or
service-hosted media), so they are out of scope here.

## What do you want to do?

| Task | Script |
| --- | --- |
| Check that credentials and consent work | [`quickstart.py`](./quickstart.py) |
| Put a colleague list on one presence board, as CSV | [`presence/team_status.py`](./presence/team_status.py) |
| Read, override or annotate your own presence | [`presence/status.py`](./presence/status.py) |
| Watch a desk and act when someone becomes free | [`presence/monitor.py`](./presence/monitor.py) |
| Book meetings idempotently — one, or a CSV of many | [`meetings/book.py`](./meetings/book.py) |
| Find a meeting by its join link, retitle it or cancel it | [`meetings/manage.py`](./meetings/manage.py) |
| See which recordings, transcripts and attendance a meeting has | [`meetings/artifacts.py`](./meetings/artifacts.py) |
| Review PSTN quality: where the failed calls ended | [`callrecords/direct_routing.py`](./callrecords/direct_routing.py) |
| List recent calls, or walk one call down to its media segments | [`callrecords/list.py`](./callrecords/list.py), [`sessions.py`](./callrecords/sessions.py) |

## Start here

```bash
cp .env.example .env
uv run python examples/communications/quickstart.py
```

→ [`quickstart.py`](./quickstart.py) connects and reads your own presence. If it
prints a status, your app registration and consent are fine.

## Presence — is this person reachable?

[`presence/`](./presence/) · `Presence.Read` (own) · `Presence.Read.All` (anyone) · `Presence.ReadWrite` (change)

One resource per user, kept current by Teams. Read one user, read 650 at once,
or override your own status for a fixed window.

```python
presence = client.me.presence.get().execute_query()
print(presence.availability, presence.activity)  # e.g. Busy / InACall

# the bulk action takes user object ids; the by-name call resolves them first
for presence in client.communications.get_presences_by_principal_name(upns).execute_query():
    print(presence.id, presence.availability)
```

→ [`status.py`](./presence/status.py) reads, sets, annotates and clears your own;
[`team_status.py`](./presence/team_status.py) resolves the UPNs you list and exports the
whole board as CSV, one presence request.

## Online meetings — join links without a calendar

[`meetings/`](./meetings/) · `OnlineMeetings.ReadWrite`

An online meeting is *not* a calendar event: you get a `joinWebUrl` and nothing
lands in anyone's inbox. Post the link as an event body if you do want an invite
([`../outlook/events/online_meeting.py`](../outlook/events/online_meeting.py)).

```python
meeting = client.me.online_meetings.create(
    subject="Project sync", start_datetime=start, end_datetime=end
).execute_query()
print(meeting.join_web_url)
```

Idempotent creation is available too — `create_or_get(external_id=…)` returns the
existing meeting when your external id is already known, which makes retries and
booking syncs safe.

→ [`book.py`](./meetings/book.py) books from flags or from a CSV, one `create_or_get` per
row; [`manage.py`](./meetings/manage.py) resolves a meeting by the `joinWebUrl` on a ticket
and retitles, moves or cancels it — printing the change unless you pass `--apply`.

## Call records — call quality and PSTN

[`callrecords/`](./callrecords/) · `CallRecords.Read.All` (application)

A record is the call, a **session** is one endpoint's leg, a **segment** is a
media stream inside it. Records are retained for 30 days and the feed rejects
`$top`, so filter on `startDateTime`. Direct Routing calls are a flat log
(`get_direct_routing_calls`) rather than entities.

## Why is this folder not under `teams/`?

Because it is not the Teams API. Presence, online meetings and call records are
their own Graph namespace — `client.communications` — with their own endpoint and
their own scopes, and this tree mirrors the client: one folder per namespace. The
only overlap with the product is online meetings, so [`../teams/`](../teams/)
links here instead of duplicating the code.

## Virtual events — wired, but not exercised here

`client.solutions.virtual_events` (town halls, webinars, their registrations,
presenters and sessions) is part of this namespace in the library, and the path
resolves: `/solutions/virtualEvents/townhalls`. Reading it needs
`VirtualEvent.Read.All` — the `.ReadWrite` variants to create — plus a Teams
Premium licence, and our test tenant answers `403 Insufficient permissions`. So
there is no script here that we could actually run; the model is there and the
first tenant that grants the scope can read it.

## Official docs

- [Cloud communications API overview](https://learn.microsoft.com/en-us/graph/api/resources/communications-api-overview)
- [Presence API](https://learn.microsoft.com/en-us/graph/api/resources/presence)
- [Online meetings](https://learn.microsoft.com/en-us/graph/api/resources/onlinemeeting)
- [Call records API](https://learn.microsoft.com/en-us/graph/api/resources/callrecords-api-overview)
