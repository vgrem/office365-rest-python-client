"""Site permissions matrix.

Lists the role definitions (permission levels) with their decoded base
permissions, then the principals (users/groups) granted access to the site
via role assignments and the roles bound to each. Grants of the Full Control
role are flagged as over-privileged.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

FULL_CONTROL = "Full Control"


def main():
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    role_defs = ctx.web.role_definitions.get().execute_query()
    print(f"Role definitions ({len(role_defs)}):")
    for rd in role_defs:
        perms = ", ".join(rd.base_permissions.permission_levels)
        print(f"  {rd.name:30s} perms=[{perms}]")

    assignments = ctx.web.role_assignments.expand(["Member", "RoleDefinitionBindings"]).get().execute_query()
    print(f"\nRole assignments ({len(assignments)}):")
    full_control_holders = 0
    for ra in sorted(assignments, key=lambda a: a.member.title or ""):
        roles = [r.name for r in ra.role_definition_bindings if r.name]
        principal = ra.member
        marker = "  <-- Full Control" if FULL_CONTROL in roles else ""
        if marker:
            full_control_holders += 1
        print(f"  {principal.title:35s} ({principal.principal_type_name})  roles: {', '.join(roles)}{marker}")

    print(
        f"\nTotal: {len(role_defs)} role definitions, {len(assignments)} assignments, "
        f"{full_control_holders} principal(s) with Full Control"
    )


if __name__ == "__main__":
    main()
