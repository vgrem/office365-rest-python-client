"""
Mailbox report: automatic reply status per mailbox user.

``mailboxSettings`` is an Exchange-backed property, so listing it in a
``$select`` on the ``/users`` collection can fail with
``ExplicitTargetMailboxIdShouldNotBeNullOrWhiteSpace`` (users without a
mailbox have no explicit target mailbox id). Instead fetch it per user via
``GET /users/{id}/mailboxSettings`` and skip mailboxes that error.

Requires application permission ``User.Read.All`` (plus ``MailboxSettings.Read``).

https://learn.microsoft.com/en-us/graph/api/user-get-mailboxsettings
"""

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    users = client.users.select(["id", "displayName", "userPrincipalName"]).top(20).get().execute_query()
    print(f"Auto-reply status for {len(users)} users:\n")
    for u in users:
        status = "no mailbox"
        try:
            target = u.select(["mailboxSettings"]).get().execute_query()
            status = target.mailbox_settings.automaticRepliesSetting.status or "disabled"
        except ClientRequestException:
            pass
        print(f"  {u.display_name:30s}  auto-replies: {status}")


if __name__ == "__main__":
    main()
