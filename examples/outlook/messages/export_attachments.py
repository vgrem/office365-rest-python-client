"""
Download all attachments from a folder to local disk.

A popular backup / archive use case — walks messages with attachments and saves
each file (base64-decoding the ``contentBytes`` payload).

Requires delegated permission ``Mail.Read``.

https://learn.microsoft.com/en-us/graph/api/attachment-get
"""

import argparse
import base64
import os

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download all attachments from a folder")
    parser.add_argument("--folder", default="inbox", help="folder path or id")
    parser.add_argument("--output", default="attachments", help="output directory")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    os.makedirs(args.output, exist_ok=True)

    messages = (
        client.me.mail_folders[args.folder].messages.select(["subject", "hasAttachments"]).get_all().execute_query()
    )

    saved = 0
    for message in messages:
        if not message.has_attachments:
            continue
        for attachment in message.attachments.get().execute_query():
            content = attachment.get_property("contentBytes")
            if not content:
                continue
            name = attachment.get_property("name") or "attachment.bin"
            with open(os.path.join(args.output, name), "wb") as f:
                f.write(base64.b64decode(content))
            saved += 1
            print(f"  {name}  (from '{message.subject}')")

    print(f"Downloaded {saved} attachments to {args.output}")


if __name__ == "__main__":
    main()
