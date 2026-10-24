"""
Create a draft from a saved MIME (.eml) document.

A message on disk is already complete: Graph parses the file itself, so the recipients,
subject, date and attachments all come from its headers and nothing else needs spelling.
``add_from_mime`` base64-encodes the bytes and posts them as ``text/plain``. Exchange
creates the message as a **draft** (``isDraft`` cannot be cleared by ``PATCH``) and stamps
``receivedDateTime`` with the import time — the original date survives in the ``Date``
header, which Graph reports as ``sentDateTime``.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-messages
"""

import argparse
import pathlib

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

parser = argparse.ArgumentParser(description="Import an .eml file into a mailbox as a draft")
parser.add_argument("eml", type=pathlib.Path, help="the message file to import")
parser.add_argument("--folder", default="drafts", help="destination folder id or well-known name")
args = parser.parse_args()

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

folder = client.me.mail_folders[args.folder].get().execute_query()
draft = folder.messages.add_from_mime(args.eml.read_bytes())
draft.execute_query()

print(f"Imported: {draft.subject!r}  internetMessageId={draft.internet_message_id}  isDraft={draft.is_draft}")
