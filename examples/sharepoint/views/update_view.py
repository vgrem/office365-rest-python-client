"""
Update a view: rename it, set it as the default, hide it, and render as HTML.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Update a view")
    parser.add_argument("--view", required=True, help="View title")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--new-title", help="New view title")
    parser.add_argument("--make-default", action="store_true", help="Set this view as the default")
    parser.add_argument("--hide", action="store_true", help="Hide the view")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    view = ctx.web.lists.get_by_title(args.list_title).views.get_by_title(args.view)
    if args.new_title:
        view.set_property("Title", args.new_title)
    if args.make_default:
        view.set_property("DefaultView", True)
    if args.hide:
        view.set_property("Hidden", True)
    view.update().execute_query()
    print(f"View updated: {view.title}")

    html = view.render_as_html().execute_query()
    print(f"Rendered HTML length: {len(html.value)}")


if __name__ == "__main__":
    main()
