"""
Document lifecycle — check out, edit, and check in a file.

SharePoint document libraries require check-out/check-in for version
control. This workflow prevents others from editing simultaneously
and keeps a clean version history with comments.

Pattern: checkout → upload edits → checkin with comment.

Requires delegated permission ``Files.ReadWrite`` or ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/driveitem-checkout
https://learn.microsoft.com/en-us/graph/api/driveitem-checkin
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: find a SharePoint document library or use OneDrive --
    # Use the root of the default drive (OneDrive) for simplicity.
    # For a SharePoint library, replace with:
    #   site = client.sites.get_by_url("https://contoso.sharepoint.com/sites/TeamSite")
    #   lib = site.drive  # or site.drives["Documents"]

    drive = client.me.drive
    root = drive.root.get().execute_query()
    print(f"Drive: {drive.owner.display_name or '?'}\n")

    # -- Step 2: create or find a test document --
    target = root.get_by_path("checkout_test.txt")
    try:
        existing = target.get().execute_query()
        print(f"File exists: {existing.name}")
    except Exception:
        print("Creating test file...")
        target = root.upload("checkout_test.txt", b"Original content\n").execute_query()
        print(f"Created: {target.name}")

    # Reload to get the ID and drive reference
    item = target.get().execute_query()

    # -- Step 3: check out the file --
    print("\nChecking out...")
    item.checkout().execute_query()
    print("  ✓ Checked out (others can't edit)")

    # -- Step 4: upload an updated version --
    print("Uploading updated version...")
    item = item.upload("checkout_test.txt", b"Original content\n\nUpdated content.\n").execute_query()
    print("  ✓ Uploaded new version")

    # -- Step 5: check in with a comment --
    print("Checking in...")
    item.checkin(comment="Fixed typos and added section 2", checkin_as="published").execute_query()
    print("  ✓ Checked in (version published)")

    # -- Step 6: verify version history --
    versions = item.versions.get().execute_query()
    print(f"\nVersion history ({len(versions)} versions):")
    for v in versions:
        dt = v.last_modified_date_time.strftime("%Y-%m-%d %H:%M") if v.last_modified_date_time else "?"
        label = v.label or "(no label)"
        print(f"  v{label or '?'}  {dt}")

    # -- Cleanup: discard checkout test if interrupted --
    # If something went wrong and the file is still checked out:
    #   item.discard_checkout().execute_query()


if __name__ == "__main__":
    main()
