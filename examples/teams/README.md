# Microsoft Teams

Tenant admin and management workflows for Teams via the Graph API —
audit, lifecycle, apps, channels, chats, tags, and usage reports.

---

## Audit & Governance

### [Team overview](audit_teams_overview.py)

Audit: tenant-wide Teams report with owners, member counts, visibility, and archive status.

```python
teams = client.teams.get_all().select(
    ["id", "displayName", "visibility", "mailNickname", "description"]
).execute_query()

for team in teams:
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    guests = [m for m in members if "#EXT#" in (m.properties.get("email", "") or "")]
    status = "archived" if team.is_archived else "active"
    print(f"{team.display_name}: {len(members)} members  {team.visibility}  {status}")
```


### [Settings compliance](audit_team_settings.py)

Scan team settings across the tenant for policy compliance.

```python
teams = client.teams.get_all().select(["id", "displayName"]).execute_query()

for team in teams:
    guest = team.get_property("guestSettings") or {}
    messaging = team.get_property("messagingSettings") or {}
    if guest.get("allowCreateUpdateChannels") is False:
        print(f"  {team.display_name}: guests cannot create channels")
```


### [Guest access audit](audit_guest_access.py)

Security audit: find all teams with external guest users.

```python
teams = client.teams.get_all().select(["id", "displayName"]).execute_query()

for team in teams:
    members = team.members.get().execute_query()
    guests = [m for m in members if "#EXT#" in (m.properties.get("email", "") or "")]
    if guests:
        print(f"  {team.display_name}: {len(guests)} guest(s)")
```


### [Lifecycle report](audit_lifecycle.py)

Lifecycle: report on archived and recently deleted teams.

```python
teams = client.teams.get_all().select(["id", "displayName", "deletedDateTime"]).execute_query()
archived = [t for t in teams if t.is_archived]

deleted = client.directory.deleted_teams.get().select(["id", "displayName", "deletedDateTime"]).execute_query()
print(f"Archived: {len(archived)}, recently deleted (restorable): {len(deleted)}")
```


### [Orphaned teams](audit_orphan_owners.py)

Find teams without owners — orphaned teams that no one administers.

```python
for team in client.teams.get_all().select(["id", "displayName"]).execute_query():
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    if not owners:
        print(f"  {team.display_name}")
```


### [Archive candidates](archive_lifecycle.py)

Find inactive teams and report archiving candidates.

```python
for team in client.teams.get_all().execute_query():
    last_msg = None
    for channel in team.channels.get().execute_query():
        msgs = channel.messages.top(1).order_by("createdDateTime desc").get().execute_query()
        if msgs and msgs[0].created_datetime:
            if last_msg is None or msgs[0].created_datetime > last_msg:
                last_msg = msgs[0].created_datetime
    if last_msg is None or last_msg < cutoff:
        print(f"  {team.display_name}")
```


### [Inactive channels](find_inactive_channels.py)

Find inactive channels across all teams based on last message date.

```python
for team in client.teams.get_all().execute_query():
    for channel in team.channels.get().execute_query():
        messages = channel.messages.top(1).order_by("createdDateTime desc").get().execute_query()
        last = messages[0].created_datetime if messages else None
        if last is None or last < cutoff:
            print(f"  {team.display_name} / {channel.display_name}")
```


---

## Team Management

### [Team lifecycle](manage.py)

Team lifecycle and settings management.

```python
team = client.teams.create("Sales Team", "Tracking pipeline deals").execute_query_and_wait()
print(f"Created: {team.display_name} ({team.id})")

team.archive().execute_query()        # archive
team.unarchive().execute_query()      # restore
team.delete_object().execute_query()  # delete
```


### [Membership](members/manage.py)

Team membership management.

```python
team = client.teams[team_id].get().execute_query()
user = client.users[user_ref].get().execute_query()

member = team.members.add(user=user, roles=["owner"]).execute_query()
print(f"Added: {member.properties.get('email')}")
```


---

## Apps & Tags

### [App catalog inventory](apps/catalog.py)

Inventory of apps in the tenant Teams app catalog.

```python
apps = client.app_catalogs.teams_apps.expand(["appDefinitions"]).get().execute_query()

for app in apps:
    definitions = list(app.app_definitions)
    latest = definitions[-1] if definitions else None
    state = latest.properties.get("publishingState", "?") if latest else "?"
    print(f"{app.display_name}  state={state}")
```


### [App adoption](apps/installed_apps.py)

Report on apps installed across all Microsoft Teams, with adoption metrics.

```python
for team in client.teams.get_all().execute_query():
    apps = team.installed_apps.expand(["teamsAppDefinition"]).get().execute_query()
    for app in apps:
        name = app.teams_app_definition.properties.get("displayName", "?")
        print(f"[{team.display_name}]  {name}")
```


### [App lifecycle](apps/manage.py)

Install, uninstall, and inspect Teams apps in a team.

```python
# Search the catalog for an app
apps = client.app_catalogs.teams_apps.filter("contains(displayName,'Power')").get().execute_query()

# Install it into a team
team = client.teams[team_id].get().execute_query()
bind = "https://graph.microsoft.com/v1.0/appCatalogs/teamsApps/{app_id}"
team.installed_apps.add(**{"teamsApp@odata.bind": bind}).execute_query()
```


### [Pinned apps](apps/tabs.py)

Report on tabs (pinned apps) across all Microsoft Teams.

```python
for team in client.teams.get_all().execute_query():
    for channel in team.channels.get().execute_query():
        tabs = channel.tabs.expand(["teamsApp"]).get().execute_query()
        for tab in tabs:
            app = tab.teams_app
            print(f"[{team.display_name}]  {channel.display_name}  ->  {app.display_name if app else '?'}")
```


### [Tag inventory](tags/report.py)

Report: all tags across all teams with member count, and teams without tags.

```python
for team in client.teams.get_all().execute_query():
    tags = team.tags.get().execute_query()
    for tag in tags:
        print(f"[{team.display_name}]  {tag.display_name}  ({tag.member_count} members)")
```


### [Tag management](tags/manage.py)

Teamwork tags management.

```python
team = client.teams[team_id].get().execute_query()

tag = team.tags.add(displayName="Designers", description="UX design team").execute_query()
user = client.users[user_ref].get().execute_query()
tag.members.add(userId=user.id).execute_query()
```


---

## Collaboration

### [Shared channels](channels/shared.py)

Shared channels: create, share with another team, and verify access.

```python
host = client.teams[host_id].get().execute_query()
channel = host.channels.add(
    display_name="Design",
    description="Design team sync",
    membership_type="shared",
).execute_query()

host.channels[channel.id].shared_with_teams.add(teamId=guest_id).execute_query()
```


### [Channel inventory](channels/inventory.py)

Cross-team channel inventory and audit.

```python
for team in client.teams.get_all().execute_query():
    channels = team.channels.get().execute_query()
    for ch in channels:
        print(f"{team.display_name}  {ch.display_name}  {ch.membership_type}  archived={ch.is_archived}  email={ch.email}")
```


### [Channel lifecycle](channels/manage.py)

Manage channel lifecycle: list, create, update, delete, and channel email.

```python
team = client.teams[team_id].get().execute_query()
channel = team.channels.add(
    display_name="General",
    description="Company-wide announcements",
    membership_type="standard",
).execute_query()
print(f"Created: {channel.display_name} ({channel.id})")
```


### [Channel messaging](channels/messages.py)

Channel messaging: send, reply, list, and a team-wide activity digest.

```python
team = client.teams[team_id].get().execute_query()
channel = team.channels[channel_id].get().execute_query()

message = channel.messages.add("Hello team!").execute_query()
reply = message.replies.add("Welcome aboard!").execute_query()
```


### [Empty / stale teams](find_empty_teams.py)

Find teams with no channels or no messages — cleanup candidates.

```python
for team in client.teams.get_all().execute_query():
    channels = team.channels.get().execute_query()
    if not channels:
        print(f"  EMPTY  {team.display_name}")
        continue
    msgs = channels[0].messages.top(1).get().execute_query()
    if not msgs:
        print(f"  STALE  {team.display_name}")
```


### [Excessive owners](find_excessive_admins.py)

Find teams with excessive owners — security risk and least-privilege violation.

```python
for team in client.teams.get_all().execute_query():
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    if len(owners) > 5:
        print(f"  {team.display_name}: {len(owners)} owners")
```


### [Export membership](export_membership.py)

Export all team memberships to CSV using CollectionCsvWriter.

```python
with open("teams_membership.csv", "w", newline="") as f:
    client.teams.get_all().select(
        ["displayName", "members/displayName", "members/email", "members/roles"]
    ).expand(["members"]).to_csv(f).execute_query()
```


### [Online meetings](online_meetings.py)

Create Teams online meetings with join links.

```python
meeting = client.me.online_meetings.create(
    start_datetime=datetime.now(timezone.utc) + timedelta(hours=1),
    end_datetime=datetime.now(timezone.utc) + timedelta(hours=2),
    subject="Project sync",
    lobbyBypassSettings={"scope": "organization", "isDialInBypassEnabled": False},
    allowMeetingChat="enabled",
).execute_query()
print(meeting.join_web_url)
```


---

## Chats

### [Chat inventory](chats/inventory.py)

Chat inventory for a user.

```python
user = client.me.get().execute_query()
chats = user.chats.top(20).get().execute_query()

for chat in chats:
    members = chat.members.get().execute_query()
    print(f"{chat.chat_type}  topic={chat.properties.get('topic')}  members={len(members)}")
```


### [Chat lifecycle](chats/manage.py)

Create and manage chats.

```python
user1 = client.users[user1_ref].get().execute_query()
user2 = client.users[user2_ref].get().execute_query()

chat = client.chats.add(ChatType.oneOnOne, owner_ids=[user1.id, user2.id]).execute_query()

group = client.chats.add(ChatType.group, owner_ids=[user1.id, user2.id])
group.set_property("topic", "Design team").update().execute_query()
```


### [Chat messaging](chats/messages.py)

Chat messaging: send, reply, list, export, and an activity digest.

```python
chat = client.chats[chat_id].get().execute_query()
message = chat.messages.add("Hello!").execute_query()
reply = message.replies.add("Hi there!").execute_query()
```


---

## Reports & Analytics

### [Usage reports](reports/usage.py)

Usage report: team counts and user activity over multiple periods.

```python
for p in ["D7", "D30", "D90"]:
    counts = client.reports.get_teams_team_counts(p).execute_query()
    activity = client.reports.get_teams_user_activity_counts(p).execute_query()
    print(f"{p}: {counts.value} teams, {activity.value} active users")
```


### [Call records](call_records.py)

Call records — Teams call quality analytics across the tenant.

```python
records = client.communications.call_records.get().execute_query()

for r in records:
    print(f"  {r.start_date_time}  {r.type_.name}  organizer={r.organizer}")
    for s in r.sessions.get().execute_query():
        print(f"      {s.caller} -> {s.callee}  modalities={[m.name for m in s.modalities]}")
```


---
