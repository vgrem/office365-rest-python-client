"""
Add, remove, and reorder columns in a view.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Manage view columns")
    parser.add_argument("--view", required=True, help="View title")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--add", help="Field internal name or title to add")
    parser.add_argument("--remove", help="Field internal name or title to remove")
    parser.add_argument("--move-to", type=int, help="Move the first field to this zero-based index")
    args = parser.parse_args()

    if not args.add and not args.remove and args.move_to is None:
        raise SystemExit("Provide --add, --remove, or --move-to")

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    view = target_list.views.get_by_title(args.view)
    fields = view.view_fields

    if args.add:
        fields.add_view_field(args.add).execute_query()
        print(f"Added column: {args.add}")
    if args.remove:
        fields.remove_view_field(args.remove).execute_query()
        print(f"Removed column: {args.remove}")
    if args.move_to is not None and (args.add or args.remove):
        # Move the column that was just changed to the requested position
        moved = args.add or args.remove
        fields.move_view_field_to(moved, args.move_to).execute_query()
        print(f"Moved column '{moved}' to position {args.move_to}")

    columns = view.view_fields.get().execute_query()
    print(f"View columns ({len(columns)}): {[c for c in columns]}")


if __name__ == "__main__":
    main()
