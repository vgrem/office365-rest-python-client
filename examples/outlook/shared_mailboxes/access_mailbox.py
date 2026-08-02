"""
Access a shared mailbox you don't own: read its recent messages and folders.

The key pattern: a shared mailbox is exposed as a regular user object, so
address it via ``client.users[<shared-mailbox-upn>]`` instead of ``client.me``.

Requires delegated permission ``Mail.Read`` (or app permission ``Mail.Read``).

https://learn.microsoft.com/en-us/graph/api/resources/shared-mailbox
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_shared_mailbox_upn, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = client.users[test_shared_mailbox_upn]

messages = shared.messages.top(5).get().execute_query()
print(f"Recent messages in {test_shared_mailbox_upn}:\n")
for m in messages:
    print(f"  {m.subject or '(no subject)'}")

folders = shared.mail_folders.get().execute_query()
print(f"\nFolders ({len(folders)}):")
for f in folders:
    print(f"  {f.display_name}")
