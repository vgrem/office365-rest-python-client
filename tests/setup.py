"""Guided local credential setup — run ``python -m tests.setup``.

Prompts for the minimum it needs (tenant and sign-in app id, only when they are
missing), reuses or creates a certificate and secret, derives the SharePoint
URLs from the tenant name, then generates the repo-root ``.env``. Re-running is
safe: existing credentials and ``.env`` entries are reused unless you ask for new
ones.

Prerequisite: an app registration that allows public client flows and has the
delegated ``Application.ReadWrite.All`` permission with admin consent. The app
you sign in with is the one configured, unless you pass ``--new-app``.

``--grant`` goes one step further and closes the loop: it reads the permissions the
live suites declare (through :mod:`tests.preflight`), asks before changing anything,
grants what the signed-in administrator is allowed to grant, and re-reads the tenant to
show what is left. Sign in with an account holding **Global Administrator** or
**Privileged Role Administrator** — consent for delegated scopes and application roles is
a tenant-wide change, and the wizard says so before it makes it.

Examples::

    python -m tests.setup
    python -m tests.setup --dry-run
    python -m tests.setup --sites selected --site https://contoso.sharepoint.com/sites/team
    python -m tests.setup --with-secret --new-app --app-name my-app
    python -m tests.setup -y --tenant contoso.onmicrosoft.com --client-id <app-id>
    python -m tests.setup --grant --admin vadimadm@contoso.onmicrosoft.com
"""

from __future__ import annotations

import argparse
import getpass
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypeVar

from office365.directory.applications.application import Application
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException

from tests import preflight
from tests.capabilities import forget_cached_tenant_facts
from tests.settings import ENV, Settings, derived_urls, settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = Path(__file__).resolve().parent
CERT_PUBLIC = TEST_DIR / "selfsigncert.crt"
CERT_PRIVATE = TEST_DIR / "selfsigncert.pem"
ENV_BAK = PROJECT_ROOT / ".env.bak"

DEFAULT_APP_NAME = "office365-rest-python-client"
_T = TypeVar("_T")


@dataclass
class _Options:
    tenant: str
    client_id: str
    admin: str
    app_name: str
    create_new: bool
    interactive: bool
    force: bool
    generate_cert: bool
    reuse_cert: bool
    want_secret: bool
    rotate_secret: str | None
    sites_scope: str
    site_urls: list[str]
    extras: bool
    username: str
    username_alt: str
    shared_mailbox: str
    password: str


# --------------------------------------------------------------------------- #
# Prompts
# --------------------------------------------------------------------------- #
def _ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    reply = input(f"{prompt}{suffix}: ").strip()
    return reply or default


def _ask_yes_no(prompt: str, *, default: bool = False) -> bool:
    hint = "Y/n" if default else "y/N"
    reply = input(f"{prompt} [{hint}]: ").strip().lower()
    if not reply:
        return default
    return reply in ("y", "yes")


def _ask_password() -> str:
    return getpass.getpass("OFFICE365_PASSWORD (blank to skip): ").strip()


def _ask_site_urls() -> list[str]:
    print("Enter SharePoint site URLs (blank to finish):")
    urls: list[str] = []
    while True:
        value = input("  site URL: ").strip()
        if not value:
            return urls
        urls.append(value)


def _pick(label: str, candidates: list[str], exclude: str | None = None) -> str:
    if candidates:
        print(f"{label}:")
        for index, upn in enumerate(candidates, 1):
            suffix = "  (you)" if upn == exclude else ""
            print(f"  {index:2d}. {upn}{suffix}")
    while True:
        reply = input(f"{label} (number, UPN, or blank to skip): ").strip()
        if not reply:
            return ""
        if reply.isdigit() and candidates and 1 <= int(reply) <= len(candidates):
            chosen = candidates[int(reply) - 1]
            if chosen == exclude:
                print("  Pick a user other than the signed-in account.")
                continue
            return chosen
        return reply


# --------------------------------------------------------------------------- #
# Certificate helpers (openssl, matching the other setup scripts)
# --------------------------------------------------------------------------- #
def _require_openssl() -> None:
    if shutil.which("openssl") is None:
        raise SystemExit("openssl is required to generate a certificate; install it and retry.")


def generate_certificate(common_name: str) -> None:
    CERT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["openssl", "genrsa", "-out", str(CERT_PRIVATE), "2048"], check=True)
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-new",
            "-key",
            str(CERT_PRIVATE),
            "-out",
            str(CERT_PUBLIC),
            "-days",
            "365",
            "-subj",
            f"/CN={common_name}",
        ],
        check=True,
    )


def cert_thumbprint() -> str:
    """Hex SHA-1 thumbprint of the local certificate (same value Entra stores)."""
    return Application.certificate_thumbprint(CERT_PUBLIC)


def _tenant_prefix(tenant: str, upn: str = "") -> str:
    """Derive the SharePoint tenant name from the tenant id/domain or the signed-in UPN."""
    if "." in tenant:
        return tenant.split(".", maxsplit=1)[0]
    if "@" in upn and "." in upn.split("@", maxsplit=1)[1]:
        return upn.split("@", maxsplit=1)[1].split(".", maxsplit=1)[0]
    if tenant and "-" not in tenant:
        return tenant
    return ""


# --------------------------------------------------------------------------- #
# .env merge
# --------------------------------------------------------------------------- #
#: ``.env`` key <- :class:`_Options` field, for the values that are set or absent.
_ENV_OF_OPTION = {
    "OFFICE365_ADMIN_USERNAME": "admin",
    "OFFICE365_USERNAME": "username",
    "OFFICE365_USERNAME_ALT": "username_alt",
    "OFFICE365_SHARED_MAILBOX_UPN": "shared_mailbox",
    "OFFICE365_PASSWORD": "password",
}


def _env_updates(opts: _Options, target_id: str, thumbprint: str, secret_value: str) -> tuple[dict, dict]:
    overrides = {"OFFICE365_TENANT": opts.tenant, "OFFICE365_CLIENT_ID": target_id}
    overrides |= {key: value for key, field in _ENV_OF_OPTION.items() if (value := getattr(opts, field))}
    if thumbprint:
        overrides["OFFICE365_CERT_THUMBPRINT"] = thumbprint
        overrides["OFFICE365_CERT_PATH"] = str(CERT_PRIVATE.relative_to(PROJECT_ROOT))
    if secret_value:
        overrides["OFFICE365_CLIENT_SECRET"] = secret_value

    derived = derived_urls(_tenant_prefix(opts.tenant, opts.username))
    defaults = {key: value for key, value in derived.items() if value}
    if opts.sites_scope == "selected" and opts.site_urls:
        defaults["OFFICE365_SITE_URL"] = opts.site_urls[0]
        defaults["OFFICE365_TEAM_SITE_URL"] = opts.site_urls[0]
    return overrides, defaults


def _protect(path: Path) -> None:
    """Keep ``.env`` to its owner: it holds an app secret and the admin account."""
    path.chmod(0o600)


def _write_env(opts: _Options, target_id: str, thumbprint: str, secret_value: str, *, dry_run: bool) -> None:
    overrides, defaults = _env_updates(opts, target_id, thumbprint, secret_value)
    text = ENV.merge(overrides, defaults)
    if dry_run:
        print("== .env (dry run; nothing written) ==")
        print(ENV.redact(text))
        return
    if ENV.path.is_file():
        shutil.copy2(ENV.path, ENV_BAK)
        _protect(ENV_BAK)
    ENV.path.write_text(text, encoding="utf-8")
    _protect(ENV.path)
    print(f"Wrote {ENV.path.relative_to(PROJECT_ROOT)} (backup: {ENV_BAK.name})")
    if not secret_value:
        print(
            "Note: the 'app-only' (client secret) flow is not configured. Create one with\n"
            "      `python -m tests.setup --with-secret`, or "
            "examples/entraid/applications/rotate_secret.py."
        )
    print("Next: python -m tests.doctor")


# --------------------------------------------------------------------------- #
# Options / Graph actions
# --------------------------------------------------------------------------- #
#: ``--flag`` name <- ``Settings`` field, for the two that are spelled differently.
_SETTINGS_FIELD = {"admin": "admin_username"}


def _required(args: argparse.Namespace, parser: argparse.ArgumentParser, attr: str, prompt: str) -> str:
    """A value the wizard cannot proceed without: flag, then ``.env``, then prompt."""
    field = _SETTINGS_FIELD.get(attr, attr)
    if value := getattr(args, attr) or getattr(settings, field):
        return value
    if args.yes:
        parser.error(f"--{attr.replace('_', '-')} is required with --yes")
    value = _ask(prompt)
    if not value:
        parser.error(f"--{attr.replace('_', '-')} is required")
    return value


def _resolve_core(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[str, str, str]:
    tenant = _required(args, parser, "tenant", "Tenant (domain or id)")
    client_id = _required(args, parser, "client_id", "Sign-in app (client) ID")
    admin = args.admin or settings.admin_username
    if args.interactive and not admin:
        admin = _required(args, parser, "admin", "Admin UPN (interactive sign-in)")
    return tenant, client_id, admin


def _resolve_sites(args: argparse.Namespace) -> tuple[str, list[str]]:
    if args.site:
        return "selected", list(args.site)
    scope = args.sites or "all"
    if scope == "selected" and not (args.yes or args.grant):
        return scope, _ask_site_urls()
    return scope, []


def _resolve_extras(args: argparse.Namespace) -> bool:
    if args.pick_users or args.with_password:
        return True
    if args.username_alt is not None or args.shared_mailbox is not None:
        return True
    if args.yes or args.grant:
        return False  # `--grant` is a request to grant, not a request for optional values
    return _ask_yes_no("Set up optional values (secondary user, shared mailbox, ROPC password)?", default=False)


def _resolve_password(args: argparse.Namespace, extras: bool) -> str:
    if args.no_password or args.yes:
        return settings.password
    if args.with_password or (extras and not settings.password):
        return _ask_password() or settings.password
    return settings.password


def _resolve_secret(args: argparse.Namespace, existing_values: dict[str, str]) -> bool:
    """Decide whether to create a client secret alongside the certificate.

    ``--no-secret`` wins, then ``--with-secret`` forces creation. An already
    configured secret is reused silently. Otherwise the user is asked once;
    non-interactive runs (``--yes``) default to no, keeping ``.env`` deterministic.
    """
    if args.no_secret:
        return False
    if args.with_secret or args.rotate_secret:
        return True
    if args.yes:
        return False
    if args.grant or existing_values.get("OFFICE365_CLIENT_SECRET") or settings.client_secret:
        return False
    return _ask_yes_no("Also create a client secret (enables the app-only flow)?", default=False)


def _resolve_options(
    args: argparse.Namespace, parser: argparse.ArgumentParser, existing_values: dict[str, str]
) -> _Options:
    tenant, client_id, admin = _resolve_core(args, parser)
    sites_scope, site_urls = _resolve_sites(args)
    extras = _resolve_extras(args)
    return _Options(
        tenant=tenant,
        client_id=client_id,
        admin=admin,
        app_name=args.app_name,
        create_new=args.new_app,
        interactive=args.interactive,
        force=args.force,
        generate_cert=args.generate_cert,
        reuse_cert=args.reuse_cert,
        want_secret=_resolve_secret(args, existing_values),
        rotate_secret=args.rotate_secret,
        sites_scope=sites_scope,
        site_urls=site_urls,
        extras=extras,
        username=args.username if args.username is not None else settings.username,
        username_alt=args.username_alt if args.username_alt is not None else settings.user_principal_alt,
        shared_mailbox=args.shared_mailbox if args.shared_mailbox is not None else settings.shared_mailbox_upn,
        password=_resolve_password(args, extras),
    )


def _try(call: Callable[[], _T], fallback: _T) -> _T:
    """A discovery call the wizard can live without: a missing grant answers ``fallback``."""
    try:
        return call()
    except ClientRequestException as exc:
        print(f"  (lookup skipped: {str(exc).splitlines()[0] or exc.__class__.__name__})")
        return fallback


def _signed_in_upn(client: GraphClient) -> str:
    me = _try(lambda: client.me.get().execute_query(), None)
    return me.user_principal_name or "" if me is not None else ""


def _list_users(client: GraphClient, limit: int = 25) -> list[str]:
    """UPNs offered as candidates when picking the secondary user / shared mailbox."""
    users = _try(lambda: client.users.select(["userPrincipalName"]).top(limit).get().execute_query(), None)
    return [user.user_principal_name for user in users or [] if user.user_principal_name]


def _apply_discovery(opts: _Options, upn: str) -> None:
    if upn and not opts.admin:
        opts.admin = upn
    if upn and not opts.username:
        opts.username = upn


def _prompt_optional_users(client: GraphClient, opts: _Options) -> None:
    if opts.username_alt and opts.shared_mailbox:
        return
    candidates = _list_users(client)
    if not opts.username_alt:
        opts.username_alt = _pick("OFFICE365_USERNAME_ALT", candidates, exclude=opts.username)
    if not opts.shared_mailbox:
        opts.shared_mailbox = _pick("OFFICE365_SHARED_MAILBOX_UPN", candidates)


def _needs_sign_in(opts: _Options, existing_values: dict[str, str]) -> bool:
    if opts.create_new or opts.force or opts.generate_cert or opts.want_secret or opts.rotate_secret or opts.extras:
        return True
    cert_ready = bool(existing_values.get("OFFICE365_CERT_THUMBPRINT")) and CERT_PRIVATE.is_file()
    return not cert_ready


def _sign_in(opts: _Options) -> GraphClient:
    client = GraphClient(tenant=opts.tenant)
    if opts.interactive:
        client = client.with_token_interactive(opts.client_id, opts.admin)
    else:
        client = client.with_device_flow(opts.client_id)
    try:
        client.require_role("Global Administrator", "Privileged Role Administrator")
    except SystemExit:
        print("  (continuing; the admin role could not be verified)")
    return client


def _ensure_certificate(client: GraphClient, app, target_id: str, display_name: str, opts: _Options) -> str:
    local_exists = CERT_PUBLIC.is_file() and CERT_PRIVATE.is_file()
    existing_keys = {key.customKeyIdentifier.upper() for key in app.key_credentials if key.customKeyIdentifier}
    local_thumb = cert_thumbprint().upper() if local_exists else ""
    already_uploaded = bool(local_thumb) and local_thumb in existing_keys

    if opts.reuse_cert and local_exists and already_uploaded and not opts.force and not opts.generate_cert:
        print("Certificate already uploaded; reusing.")
        return cert_thumbprint()

    if opts.force or opts.generate_cert or not local_exists:
        _require_openssl()
        generate_certificate(display_name)
        print(f"Generated {CERT_PUBLIC.relative_to(PROJECT_ROOT)}")
    else:
        print("Uploading the existing local certificate.")
    client.applications.get_by_app_id(target_id).ensure_certificate(CERT_PUBLIC, display_name).execute_query()
    return cert_thumbprint()


def _ensure_secret(
    client: GraphClient, target_id: str, display_name: str, existing_values: dict[str, str], opts: _Options
) -> str:
    secret_value = existing_values.get("OFFICE365_CLIENT_SECRET", "")
    if not opts.want_secret:
        return secret_value
    if secret_value and not opts.rotate_secret:
        print("Reusing the client secret already in .env.")
        return secret_value
    if opts.rotate_secret:
        client.applications.get_by_app_id(target_id).remove_password(opts.rotate_secret).execute_query()
        print(f"Removed secret {opts.rotate_secret}.")
    result = client.applications.get_by_app_id(target_id).add_password(display_name).execute_query()
    print("Created a new client secret.")
    return result.value.secretText


def _configure_credentials(client: GraphClient, opts: _Options, existing_values: dict[str, str]) -> tuple[str, str, str]:
    if opts.create_new:
        app = client.applications.ensure(opts.app_name).execute_query()
        print(f"Ensured app '{app.display_name}' ({app.app_id})")
    else:
        app = client.applications.get_by_app_id(opts.client_id).get().execute_query()
    target_id = app.app_id
    client.service_principals.ensure(target_id).execute_query()

    display_name = getattr(app, "display_name", None) or opts.app_name
    thumbprint = _ensure_certificate(client, app, target_id, display_name, opts)
    secret_value = _ensure_secret(client, target_id, display_name, existing_values, opts)
    return target_id, thumbprint, secret_value


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
#: The groups this wizard can grant. The others are names of things, not grants: a
#: directory role is assigned to a user, a license has to be bought before it can be given.
GRANTABLE = ("delegated", "application")

_MANUAL_HINT = {
    "directory role": "assign it to the test user in the Entra portal (needs Entra ID P1/P2)",
    "license": "buy seats, then assign the SKU to the test user",
}


def _apply_grants(client: GraphClient, app_id: str, plan: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    """Grant what ``plan`` asks for; return (done, failed) as human-readable lines."""
    checks = {
        "delegated": client.has_delegated_permission,
        "application": client.has_application_permissions,
    }
    grants = {
        "delegated": client.grant_delegated_permissions,
        "application": client.grant_application_permissions,
    }
    done: list[str] = []
    failed: list[str] = []
    for label in GRANTABLE:
        for name in plan.get(label, []):
            entry = f"{label} {name}"
            try:
                already = checks[label](name, app_id)
            except ClientRequestException:
                already = False  # cannot read the grants; try the grant, which is idempotent
            if already:
                done.append(f"{entry} (already granted)")
                continue
            try:
                grants[label](app_id, name).execute_query()
            except ClientRequestException as exc:
                reason = str(exc).splitlines()[0] or exc.__class__.__name__
                failed.append(f"{entry}: {reason}")
                continue
            done.append(entry)
    return done, failed


def _grant_missing(opts: _Options, args: argparse.Namespace) -> int:
    """Read what the suites need, grant what is missing, then read the tenant again."""
    cfg = Settings.from_env()
    found = preflight.suites()
    states = preflight.verify(found, opts.client_id, cfg)
    if not states:
        print("Nothing was verified: no auth flow is configured yet. Run `python -m tests.setup` first.")
        return 1

    plan = preflight.grant_plan(found, states)
    if not plan:
        print(f"Every declared permission is already granted to {opts.client_id or 'the app'}.")
        return 0

    print(f"\nPermissions the live suites declare and {opts.client_id} lacks:")
    print(preflight.render_plan(plan))
    manual = [label for label in plan if label not in GRANTABLE]
    for label in manual:
        print(f"  ({label}: {_MANUAL_HINT.get(label, 'configure it by hand')})")
    if args.dry_run:
        print("\n(dry run: nothing granted)")
        return 0
    if not args.yes and not _ask_yes_no(f"Grant these to {opts.client_id} now?", default=False):
        print("Nothing granted.")
        return 0

    client = _sign_in(opts)
    done, failed = _apply_grants(client, opts.client_id, plan)
    for line in done:
        print(f"  granted: {line}")
    for line in failed:
        print(f"  failed:  {line}")

    forget_cached_tenant_facts()
    remaining = preflight.grant_plan(found, preflight.verify(found, opts.client_id, cfg))
    if remaining:
        print("\nStill missing:")
        print(preflight.render_plan(remaining))
        print("Re-run `python -m tests.preflight --verify` once the rest is in place.")
        return 1
    print("\nEvery declared permission is now granted. `python -m tests.preflight --verify` will confirm it.")
    return 1 if failed else 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate .env for local test/example authentication.")
    parser.add_argument("--tenant", help="tenant domain or id (prompted when missing)")
    parser.add_argument("--client-id", dest="client_id", help="app id used to sign in (and, by default, configure)")
    parser.add_argument("--admin", help="admin UPN (interactive sign-in and .env)")
    parser.add_argument("--interactive", action="store_true", help="browser sign-in instead of the device code flow")
    parser.add_argument("--new-app", action="store_true", help="provision or reuse a dedicated app (by --app-name)")
    parser.add_argument(
        "--app-name", default=DEFAULT_APP_NAME, help="display name for the dedicated app (--new-app) / certificate"
    )
    parser.add_argument("--reuse-cert", action="store_true", help="keep the existing local certificate")
    parser.add_argument("--generate-cert", action="store_true", help="generate a new certificate")
    parser.add_argument("--force", action="store_true", help="regenerate and re-upload the certificate")
    parser.add_argument("--with-secret", action="store_true", help="also create a client secret")
    parser.add_argument("--no-secret", action="store_true", help="do not create a client secret")
    parser.add_argument(
        "--rotate-secret", metavar="KEY_ID", help="delete this existing secret id before creating a new one"
    )
    parser.add_argument("--sites", choices=["all", "selected"], help="SharePoint scope written to .env (default: all)")
    parser.add_argument("--site", action="append", default=[], metavar="URL", help="SharePoint site URL (repeatable)")
    parser.add_argument("--username", help="primary test user / ROPC username")
    parser.add_argument("--username-alt", dest="username_alt", help="secondary test user")
    parser.add_argument("--shared-mailbox", dest="shared_mailbox", help="shared mailbox UPN")
    parser.add_argument("--with-password", action="store_true", help="prompt for the ROPC password (hidden)")
    parser.add_argument("--no-password", action="store_true", help="keep the existing ROPC password")
    parser.add_argument(
        "--pick-users", action="store_true", help="choose secondary user / shared mailbox from the tenant"
    )
    parser.add_argument(
        "--grant",
        action="store_true",
        help="grant the permissions the live suites declare and this tenant lacks (asks first)",
    )
    parser.add_argument("--dry-run", action="store_true", help="preview the .env merge without signing in or writing")
    parser.add_argument("-y", "--yes", action="store_true", help="accept defaults; never prompt")
    return parser


def _dry_run(opts: _Options, existing_values: dict[str, str]) -> None:
    target_id = "<new-app-id>" if opts.create_new else opts.client_id
    has_cert = CERT_PUBLIC.is_file() and shutil.which("openssl") is not None
    thumbprint = cert_thumbprint() if has_cert else "<thumbprint>"
    secret_value = ""
    if opts.want_secret:
        secret_value = existing_values.get("OFFICE365_CLIENT_SECRET") or "<created-at-setup>"
    _write_env(opts, target_id, thumbprint, secret_value, dry_run=True)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    existing_values = ENV.read()
    opts = _resolve_options(args, parser, existing_values)

    print(settings.format_readiness())

    if args.grant and args.dry_run:
        return _grant_missing(opts, args)  # the plan only: no sign-in, no grants
    if args.dry_run:
        _dry_run(opts, existing_values)
        return 0

    if not _needs_sign_in(opts, existing_values):
        print("Credentials already configured; refreshing .env.")
        _write_env(
            opts,
            opts.client_id,
            existing_values.get("OFFICE365_CERT_THUMBPRINT", ""),
            existing_values.get("OFFICE365_CLIENT_SECRET", ""),
            dry_run=False,
        )
        return _grant_missing(opts, args) if args.grant else 0

    client = _sign_in(opts)
    _apply_discovery(opts, _signed_in_upn(client))
    if opts.extras:
        _prompt_optional_users(client, opts)
    target_id, thumbprint, secret_value = _configure_credentials(client, opts, existing_values)
    _write_env(opts, target_id, thumbprint, secret_value, dry_run=False)
    return _grant_missing(opts, args) if args.grant else 0


if __name__ == "__main__":
    try:
        code = main()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        code = 130
    raise SystemExit(code)
