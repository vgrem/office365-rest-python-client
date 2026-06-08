"""
Report on folders with unique permissions across a SharePoint site.

Traverses all folders in a document library and identifies those
that have broken permission inheritance — a common security and
governance concern. Useful for audits and cleanup of overly
permissioned folder structures.

Inspired by Report-PermissionsFolderLevel.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Sites.Read.All          Read site, library, and folder structures
    Sites.FullControl.All   (if reading role assignments is needed)

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.type import PrincipalType
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

_MAX_MEMBERS = 5


def scan_folder_permissions(ctx: ClientContext, folder_url: str, indent: int = 0) -> list[dict]:
    """Recursively scan folders for unique permissions.

    Args:
        ctx: Authenticated ClientContext.
        folder_url: Server-relative URL of the folder to scan.
        indent: Nesting level for display.

    Returns:
        List of dicts with folder path, inherited status, and role assignments.
    """
    results = []

    try:
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        folder_item = folder.list_item_all_fields

        # Check if permissions are unique
        has_unique = folder_item.has_unique_role_assignments  # property
        # Alternative: compare with role assignments
        role_assignments = folder_item.role_assignments.expand(["Member"]).get().execute_query()

        if has_unique:
            members = []
            for ra in role_assignments:
                member_name = getattr(ra.member, "title", str(ra.member))
                member_type = "Group" if ra.member.principal_type == PrincipalType.SharePointGroup else "User"
                members.append(f"{member_name} ({member_type})")

            results.append(
                {
                    "path": folder_url,
                    "has_unique_permissions": True,
                    "role_assignment_count": len(role_assignments),
                    "members": members,
                }
            )

        # Recurse into subfolders
        sub_folders = folder.folders.get().execute_query()
        for sub in sub_folders:
            sub_url = getattr(sub, "server_relative_url", None)
            if sub_url:
                results.extend(scan_folder_permissions(ctx, sub_url, indent + 1))

    except Exception as e:
        print(f"  Error scanning {folder_url}: {e}")

    return results


def main():
    print("Scanning folders with unique permissions...\n")

    ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)

    # Start from the default document library
    lib = ctx.web.default_document_library().get().execute_query()
    library_path = getattr(lib, "server_relative_url", None)
    if not library_path:
        print("Could not resolve library path")
        return

    print(f"Scanning library: {library_path}\n")
    folders = scan_folder_permissions(ctx, library_path)

    unique = [f for f in folders if f["has_unique_permissions"]]

    if not unique:
        print("No folders with unique permissions found (all inherit from parent).")
        return

    print(f"Found {len(unique)} folders with unique permissions:\n")
    for f in sorted(unique, key=lambda x: x["path"]):
        print(f"  {f['path']}")
        print(f"    Role assignments: {f['role_assignment_count']}")
        if f["members"]:
            for m in f["members"][:_MAX_MEMBERS]:  # show up to 5
                print(f"      - {m}")
            if len(f["members"]) > _MAX_MEMBERS:
                print(f"      ... and {len(f['members']) - _MAX_MEMBERS} more")
        print()


if __name__ == "__main__":
    main()
