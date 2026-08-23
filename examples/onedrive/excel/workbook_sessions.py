"""
Workbook sessions — create, refresh, and close.

Sessions give you a consistent view of the workbook across multiple operations
and persist (or discard) changes made during the session. This is the
recommended pattern for any multi-step workbook automation.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/workbook-createsession
https://learn.microsoft.com/en-us/graph/api/workbook-refreshsession
https://learn.microsoft.com/en-us/graph/api/workbook-closesession
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="Create, refresh and close a workbook session")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    uploaded = client.me.drive.root.upload_file(str(SAMPLE_WORKBOOK)).execute_query()
    workbook = uploaded.workbook

    # -- Step 1: create a session --
    session = workbook.create_session(persist_changes=True).execute_query()
    session_id = session.value.id
    if not session_id:
        parser.error("No session id returned")
    print(f"Session created: {session_id}")

    # -- Step 2: read data inside the session --
    worksheets = workbook.worksheets.get().execute_query()
    print(f"  Worksheets visible in session: {[ws.name for ws in worksheets]}")

    # -- Step 3: refresh the session (keep it alive) --
    workbook.refresh_session(session_id).execute_query()
    print("  Session refreshed")

    # -- Step 4: close the session --
    workbook.close_session(session_id).execute_query()
    print("  Session closed")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
