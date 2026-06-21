"""
Set your own presence and status message.

Requires delegated permission Presence.ReadWrite.

https://learn.microsoft.com/en-us/graph/api/presence-setpresence
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

expires = datetime.now(timezone.utc) + timedelta(hours=2)

client.me.presence.set_user_preferred_presence(
    availability="DoNotDisturb",
    activity="InAMeeting",
    expiration_duration="PT2H",
).execute_query()
print("Presence set to DoNotDisturb")

client.me.presence.set_status_message(
    message="In a meeting — will respond later",
    expiry=expires,
).execute_query()
print("Status message updated")
