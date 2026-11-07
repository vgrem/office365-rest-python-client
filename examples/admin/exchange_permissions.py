"""
Grant, then verify, the two things the Exchange admin API needs. Run it once per tenant.

It signs in as an administrator, checks both grants, writes only what is missing, and finally
calls the API once to prove Exchange accepts them:

1. ``Exchange.ManageAsAppV2`` - an application permission on *Office 365 Exchange Online*, which
   lets the app acquire a token for ``outlook.office365.com``. Without it the token is for the
   wrong service.
2. A directory role on the app's service principal - ``Global Reader`` by default, which covers
   every endpoint this client reads. Entra resolves the role into Exchange permissions, so
   nothing is assigned inside Exchange itself.

A token with both still answers 403 for a few minutes after a fresh assignment, which is why the
last step is a call rather than a table.

Re-running is safe: a grant that is already there is reported, not rewritten. Making either grant
needs a delegated permission on the app itself - ``AppRoleAssignment.ReadWrite.All`` to grant the
application permission, ``RoleManagement.ReadWrite.Directory`` to assign the role - and when one is
missing this script names it, because a grant script cannot grant itself.

Set ``OFFICE365_TENANT``, ``OFFICE365_CLIENT_ID`` and ``OFFICE365_CLIENT_SECRET`` in ``.env``.

Requires a Global Administrator or Privileged Role Administrator to sign in, and the delegated
permissions ``AppRoleAssignment.ReadWrite.All`` and ``RoleManagement.ReadWrite.Directory``.
"""

from __future__ import annotations

import argparse

from office365.admin.exchange import ExchangeAdminClient
from office365.graph_client import GraphClient
from office365.permissions import ResourceName
from office365.runtime.client_request_exception import ClientRequestException
from tests.settings import client_id, client_secret, tenant

#: The application permission the admin API asks a token to carry.
APP_PERMISSION = "Exchange.ManageAsAppV2"

#: Delegated permission that lets this app grant an application permission at all.
GRANT_SCOPE = "AppRoleAssignment.ReadWrite.All"

#: Delegated permission that lets this app assign a directory role.
ROLE_SCOPE = "RoleManagement.ReadWrite.Directory"

#: Least-privilege directory role: every endpoint this client reads, nothing it writes.
READ_ROLE = "Global Reader"

#: The click path that supplies a delegated permission this app is short.
ADD_SCOPE = (
    "1. add {scope} to this app (Entra admin center > App registrations > API permissions >"
    " Add a permission > Microsoft Graph > Delegated), then Grant admin consent"
)


def delegated_scopes(admin: GraphClient) -> frozenset[str] | None:
    """The delegated permissions this app has been granted, or ``None`` when they are unreadable."""
    try:
        principal = admin.service_principals.get_by_app_id(client_id).select(["id"]).get().execute_query()
        grants = admin.oauth2_permission_grants.get_all().filter(f"clientId eq '{principal.id}'").execute_query()
    except ClientRequestException:
        return None
    return frozenset(name for grant in grants for name in (grant.scope or "").split())


def explain_refusal(admin: GraphClient, needed: str, fixes: list[str]) -> None:
    """Say whether the app is short the delegated permission, then list what closes the gap."""
    scopes = delegated_scopes(admin)
    if scopes is not None and needed not in scopes:
        print(f"  this app holds no delegated grant for {needed}, which this write needs")
    for fix in fixes:
        print(f"  {fix}")


def ensure_app_permission(admin: GraphClient) -> bool:
    """Check the application permission on the app, granting it when it is missing."""
    if admin.has_application_permissions(APP_PERMISSION, client_id, resource=ResourceName.Exchange):
        print(f"  {APP_PERMISSION:<32} already granted")
        return True
    try:
        admin.grant_application_permissions(client_id, APP_PERMISSION, resource=ResourceName.Exchange).execute_query()
    except ClientRequestException as exc:
        print(f"  {APP_PERMISSION:<32} missing, and could not be granted: {_first_line(exc)}")
        explain_refusal(
            admin,
            GRANT_SCOPE,
            [
                ADD_SCOPE.format(scope=GRANT_SCOPE),
                f"2. or Entra admin center > App registrations > this app > API permissions >"
                f" {APP_PERMISSION} > Grant admin consent",
            ],
        )
        return False
    print(f"  {APP_PERMISSION:<32} granted")
    return True


def ensure_directory_role(admin: GraphClient, role_name: str) -> bool:
    """Check the app's directory role, assigning it when it is missing."""
    principal = admin.service_principals.get_by_app_id(client_id).select(["id"]).get().execute_query()
    role = admin.directory_roles.find_by_name(role_name).execute_query()
    if not role.is_loaded:
        # ``directoryRoles`` lists only the roles a tenant has activated, so activating one and
        # assigning it in the same request is the whole operation here.
        try:
            admin.directory_roles.assign(role_name).execute_query()
        except ClientRequestException as exc:
            print(f"  {role_name:<32} could not be activated: {_first_line(exc)}")
            explain_refusal(
                admin, ROLE_SCOPE, [f"activate {role_name} in Entra admin center > Roles and administrators"]
            )
            return False
        role = admin.directory_roles.find_by_name(role_name).execute_query()
        if not role.is_loaded:
            print(f"  {role_name:<32} this tenant publishes no such role")
            return False
    # Ask the app which roles it is in: ``directoryRoles/{id}/members`` was measured to leave the
    # app's service principal out of the list while the role was already in force.
    if any(member.id == role.id for member in principal.member_of.get_all().execute_query()):
        print(f"  {role_name:<32} already assigned to the app")
        return True
    try:
        role.members.add(principal)
        admin.execute_query()
    except ClientRequestException as exc:
        print(f"  {role_name:<32} missing, and could not be assigned: {_first_line(exc)}")
        explain_refusal(
            admin,
            ROLE_SCOPE,
            [
                ADD_SCOPE.format(scope=ROLE_SCOPE),
                f"2. or Entra admin center > Roles and administrators > {role_name} > Add assignments > this app",
                "3. or, if this tenant prefers Exchange-owned role groups: New-ServicePrincipal + Add-RoleGroupMember",
            ],
        )
        return False
    print(f"  {role_name:<32} assigned to the app")
    return True


def verify() -> str | None:
    """Call the API once with the app's own credentials; answer the HTTP code when it refuses."""
    client = ExchangeAdminClient(tenant, anchor=ExchangeAdminClient.system_mailbox_anchor(tenant))
    client.with_client_secret(client_id, client_secret)
    try:
        config = client.get_organization_config().execute_query().value
    except ClientRequestException as exc:
        response = exc.response
        return str(response.status_code) if response is not None else "?"
    print(f"\nExchange answered with {config.get('Name')} - the grants work.")
    return None


def _first_line(exc: Exception) -> str:
    """The first line of a server message - the rest is advice that names no name."""
    return str(exc).splitlines()[0] or exc.__class__.__name__


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", default=READ_ROLE, help=f"directory role to assign, e.g. {READ_ROLE!r}")
    args = parser.parse_args()

    print(f"Grants the Exchange admin API needs on {client_id}:")
    admin = (
        GraphClient(tenant=tenant)
        .with_device_flow(client_id)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )
    if not ensure_app_permission(admin) or not ensure_directory_role(admin, args.role):
        print("\nExchange stays closed until the missing grant above is in place - re-run when it is.")
        return

    refusal = verify()
    if refusal is None:
        return
    if refusal == "403":
        print(
            "\nExchange answered 403 although both grants are in place: a fresh assignment takes a\n"
            "few minutes to reach Exchange, so re-run shortly. If it keeps refusing,\n"
            f"{args.role!r} may be narrower than this tenant allows:\n"
            f'    python {__file__} --role "Exchange Administrator"'
        )
    else:
        print(f"\nExchange refused the token with {refusal}: check the audience and the client secret.")


if __name__ == "__main__":
    main()
