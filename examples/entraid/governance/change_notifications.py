"""
Graph change notifications — subscribe to resource changes and manage
subscription lifecycle.

Subscriptions let your app receive push notifications when Microsoft
Graph resources change.

Requires delegated permission appropriate to the resource (e.g.
``User.Read.All`` for ``/users``).

https://learn.microsoft.com/en-us/graph/api/resources/subscription
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    notification_url = input("Notification URL (HTTPS): ").strip()
    resource = input("Resource (e.g. /users): ").strip() or "/users"
    change_type = input("Change type (e.g. updated,created,deleted): ").strip() or "updated,created,deleted"

    expiry = datetime.now(timezone.utc) + timedelta(hours=12)
    sub = client.subscriptions.add(
        changeType=change_type,
        notificationUrl=notification_url,
        resource=resource,
        expirationDateTime=expiry.isoformat(),
        clientState="secret-123",
    ).execute_query()
    print(f"Subscription created: {sub.id}  resource={sub.resource}  expires={sub.expiration_date_time}")

    subs = client.subscriptions.get().execute_query()
    print(f"\nActive subscriptions ({len(subs)}):")
    for s in subs:
        exp = s.expiration_date_time.strftime("%Y-%m-%d %H:%M") if s.expiration_date_time else "?"
        print(f"  {s.id:45s}  resource={s.resource:30s}  expires={exp}")

    new_expiry = datetime.now(timezone.utc) + timedelta(hours=24)
    sub.set_property("expirationDateTime", new_expiry.isoformat())
    sub.update().execute_query()
    print(f"\nSubscription renewed — expires: {sub.expiration_date_time}")

    sub.delete_object().execute_query()
    print("Subscription deleted.")


if __name__ == "__main__":
    main()
