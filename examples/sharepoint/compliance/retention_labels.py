"""
List the compliance tags (retention labels) published to the tenant and
inspect their settings.

Requires ``Sites.Read.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def format_tag(tag) -> str:
    """Format a compliance tag with its retention/blocking actions."""
    actions = []
    if tag.BlockDelete:
        actions.append("block delete")
    if tag.BlockEdit:
        actions.append("block edit")
    if tag.AutoDelete:
        actions.append(f"auto delete ({tag.TagDuration or '?'}d)")
    return f"  {tag.TagName or '?':35s} {tag.DisplayName or '?':35s} {', '.join(actions) or 'no action'}"


def main():
    parser = argparse.ArgumentParser(description="List compliance tags (retention labels)")
    parser.add_argument("--tag", help="Show a single tag by name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    if args.tag:
        tag = ctx.site.get_available_tag(args.tag).execute_query().value
        if not tag or not tag.TagName:
            raise SystemExit(f"Tag '{args.tag}' not found among available tags.")
        print("Compliance tag:")
        print(format_tag(tag))
        return

    tags = ctx.site.get_available_tags().execute_query().value
    print(f"Available compliance tags ({len(tags)}):\n")
    for tag in tags:
        print(format_tag(tag))


if __name__ == "__main__":
    main()
