"""
Report role assignments across a SharePoint site.

Lists who (users/groups) holds which role on the site and, optionally, on
each list — useful for access reviews and least-privilege audits.

Requires read access; role assignments need Sites.FullControl.All or an
owner-level account.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

import argparse
from typing import List

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.type import PrincipalType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

MAX_MEMBERS = 10


def _assignment_rows(role_assignments) -> List[str]:
    """Render role assignments as 'member (type): role1, role2' lines."""
    rows = []
    for ra in role_assignments:
        member = ra.member
        member_type = "Group" if getattr(member, "principal_type", None) == PrincipalType.SharePointGroup else "User"
        member_name = getattr(member, "title", None) or str(member)
        roles = [r.name for r in ra.role_definition_bindings]
        rows.append(f"  {member_name} ({member_type}): {', '.join(roles) or '?'}")
    return rows


def _print_securable(label: str, securable) -> None:
    assignments = securable.role_assignments.expand(["Member", "RoleDefinitionBindings"]).get().execute_query()
    unique = "unique" if securable.has_unique_role_assignments else "inherited"
    print(f"{label}  ({len(assignments)} assignment(s), {unique}):")
    for row in _assignment_rows(assignments)[:MAX_MEMBERS]:
        print(row)
    if len(assignments) > MAX_MEMBERS:
        print(f"  ... and {len(assignments) - MAX_MEMBERS} more")
    print()


def main():
    parser = argparse.ArgumentParser(description="Report role assignments across a site")
    parser.add_argument("--list", dest="list_title", default=None, help="report only this list")
    parser.add_argument("--all-lists", action="store_true", help="report every (non-hidden) list")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    _print_securable("Site:", ctx.web)

    if args.list_title:
        _print_securable(f"List: {args.list_title}", ctx.web.lists.get_by_title(args.list_title))
    elif args.all_lists:
        for lst in ctx.web.lists.get().execute_query():
            if lst.hidden:
                continue
            _print_securable(f"List: {lst.title}", lst)


if __name__ == "__main__":
    main()
