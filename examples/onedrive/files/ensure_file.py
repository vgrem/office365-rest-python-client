"""
Provision a file idempotently with ``DriveItem.ensure_file``.

Ensures a file exists at a nested path under a throwaway folder. The first call
creates the missing folders and uploads the content; a second call is a no-op
(``on_conflict="skip"``, the default), while ``on_conflict="replace"`` overwrites
it. The whole chain — folder creation, existence check, upload — runs on a
single ``execute_query()``.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-put-content
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Ensure a file exists in OneDrive")
    parser.add_argument("--keep", action="store_true", help="keep the file after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    root = client.me.drive.root.create_folder(create_unique_name("Provision")).execute_query()
    path = "config/settings.json"

    initial = root.ensure_file(path, '{"version": 1}').execute_query()
    print(f"Ensured '{initial.name}' (id: {initial.id}, {initial.size} bytes)")

    # A second run reuses the existing file: the content is never re-sent
    again = root.ensure_file(path, '{"version": 1}').execute_query()
    print(f"Re-run was a no-op: {again.id == initial.id}")

    # Overwrite the content explicitly in a single request
    replaced = root.ensure_file(path, '{"version": 2, "note": "replaced"}', on_conflict="replace").execute_query()
    print(f"Replaced content: {initial.size} -> {replaced.size} bytes")

    if not args.keep:
        root.delete_object().execute_query()
        print("Folder removed.")


if __name__ == "__main__":
    main()
