"""
Download the MIME (.eml) representation of a message.

Saves the message as an eml file openable in any email client.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/outlook-get-mime-message
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

messages = client.me.messages.select(["id", "subject"]).top(1).get().execute_query()
with tempfile.TemporaryDirectory() as local_path:
    for message in messages:
        with open(os.path.join(local_path, message.subject + ".eml"), "wb") as f:
            message.download(f).execute_query()
        print(f"Downloaded: {f.name}")
