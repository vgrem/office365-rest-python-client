"""
Graph change notifications (webhook subscriptions) — subscribe to
resource changes and manage subscription lifecycle.

Subscriptions let your application receive push notifications when
Microsoft Graph resources change — users created, groups updated,
messages received, files modified.

This example covers:
  - Create a subscription on a resource (e.g. users, messages)
  - List existing subscriptions
  - Renew (update expiration) a subscription
  - Delete a subscription
  - Reauthorize a subscription (for encrypted content)

Requires delegated permission appropriate to the resource. For
``/users`` subscriptions you need ``User.Read.All``. For
``/me/mailFolders('inbox')/messages`` you need ``Mail.Read``.

https://learn.microsoft.com/en-us/graph/api/resources/subscription
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

# Your application's notification endpoint (must be HTTPS)
NOTIFICATION_URL = "https://your-app.ngrok.io/api/notifications"

# The resource to watch (Graph API path)
# Examples:
#   "/users"                    — user create/update/delete
#   "/groups"                   — group changes
#   "/me/mailFolders('inbox')/messages"  — new mail
#   "/drives/{drive-id}/root"   — OneDrive file changes
RESOURCE = "/users"
CHANGE_TYPE = "updated,created,deleted"


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: create a subscription --
    expiry = datetime.now(timezone.utc) + timedelta(hours=12)
    sub = client.subscriptions.add(
        changeType=CHANGE_TYPE,
        notificationUrl=NOTIFICATION_URL,
        resource=RESOURCE,
        expirationDateTime=expiry.isoformat(),
        clientState="secret-123",  # verify notifications in your handler
    ).execute_query()
    print("Subscription created:")
    print(f"  ID:             {sub.id}")
    print(f"  Resource:       {sub.resource}")
    print(f"  Change type:    {sub.change_type}")
    print(f"  Expiration:     {sub.expiration_date_time.strftime('%Y-%m-%d %H:%M')}")
    if sub.latest_supported_tls_version:
        print(f"  TLS version:    {sub.latest_supported_tls_version}")
    print()

    # -- Step 2: list all subscriptions --
    subs = client.subscriptions.get().execute_query()
    print(f"Active subscriptions ({len(subs)}):")
    for s in subs:
        exp = s.expiration_date_time.strftime("%Y-%m-%d %H:%M") if s.expiration_date_time else "?"
        print(f"  {s.id:45s}  resource={s.resource:30s}  expires={exp}")
    print()

    # -- Step 3: renew (extend expiration) --
    new_expiry = datetime.now(timezone.utc) + timedelta(hours=24)
    sub.set_property("expirationDateTime", new_expiry.isoformat())
    sub.update().execute_query()
    print("Subscription renewed — new expiration:")
    print(f"  {sub.expiration_date_time.strftime('%Y-%m-%d %H:%M')}")
    print()

    # -- Step 4: reauthorize (for encrypted content) --
    # Required when subscription includes `includeResourceData=True`
    # sub.reauthorize().execute_query()
    # print("Subscription reauthorized.")

    # -- Step 5: delete the subscription --
    sub.delete_object().execute_query()
    print("Subscription deleted.")


if __name__ == "__main__":
    main()
