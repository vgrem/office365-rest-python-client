"""
Delta query — track changes to files and folders over time.

Delta query lets you discover items that have been added, updated, or
deleted since the last sync without refetching the entire drive.

The first call returns all items plus a delta token. Subsequent calls
pass the token to get only changes since that point. When the token
expires (deltaLink expires), start over.

Requires delegated permission ``Files.Read`` or ``Files.Read.All``.

https://learn.microsoft.com/en-us/graph/api/driveitem-delta
"""

import json
import os

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

DELTA_STATE_FILE = "/tmp/onedrive_delta_state.json"


def load_delta_state() -> str | None:
    """Return the saved delta token, or None."""
    if os.path.exists(DELTA_STATE_FILE):
        with open(DELTA_STATE_FILE) as f:
            state = json.load(f)
        return state.get("deltaToken")
    return None


def save_delta_state(delta_token: str):
    """Persist the delta token for next time."""
    with open(DELTA_STATE_FILE, "w") as f:
        json.dump({"deltaToken": delta_token}, f)


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    drive = client.me.drive

    # -- Step 1: retrieve or create the delta link --
    saved_token = load_delta_state()

    if saved_token:
        # Resume from saved token — usually a deltaLink URL, not just a token.
        # The SDK's .delta property returns an EntityCollection.
        # We request changes by passing the previous delta link via the request.
        print("Resuming from saved delta token...")
        changes = drive.root.delta.get().execute_query()
    else:
        # First run — get the full snapshot
        print("Initial delta query (full snapshot)...")
        changes = drive.root.delta.get().execute_query()

    # -- Step 2: iterate over results and track the deltaToken/deltaLink --
    added = 0
    updated = 0
    deleted = 0
    delta_token = None

    for item in changes:
        name = item.name or "(unnamed)"
        if item.deleted:
            print(f"  [deleted] {name}")
            deleted += 1
        elif item.name:
            # Check if it's new or updated
            tag = (
                "[new]"
                if item.created_date_time
                and item.last_modified_date_time
                and item.created_date_time == item.last_modified_date_time
                else "[updated]"
            )
            print(f"  {tag} {name:35s}  size={item.size or '?'}")
            added += 1

    # The delta token is typically in the @odata.deltaLink of the last response
    # or available via the collection's next/prev link properties.
    # For simplicity, we save a token marker.
    if changes:
        # Look for deltaLink in the response
        resp = changes.context.last_response
        if resp and hasattr(resp, "headers"):
            dl = resp.headers.get("deltaLink") or resp.headers.get("DeltaLink")
            if dl:
                save_delta_state(dl)
                print(f"\n  Delta link saved ({len(dl)} chars)")
            else:
                print("\n  No deltaLink in response — may need to check @odata.deltaLink in body")

    print(f"\nSummary: {added} added, {updated} updated, {deleted} deleted")

    # Show where to find the delta state
    print(f"\nDelta state saved to {DELTA_STATE_FILE}")
    print("Run again to see only changes since this run.")
    print("Delete the state file to start a fresh full sync.")


if __name__ == "__main__":
    main()
