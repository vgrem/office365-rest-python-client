"""Guided local credential setup — run ``python -m tests.setup``.

Prompts for the minimum it needs (tenant and sign-in app id, only when they are
missing), reuses or creates a certificate and secret, derives the SharePoint
URLs from the tenant name, then generates the repo-root ``.env``. Re-running is
safe: existing credentials and ``.env`` entries are reused unless you ask for new
ones.

Prerequisite: an app registration that allows public client flows and has the
delegated ``Application.ReadWrite.All`` permission with admin consent. The app
you sign in with is the one configured, unless you pass ``--new-app``.

Permissions are **not** granted here. Use
``examples/entraid/applications/grant_application_perms.py`` and
``examples/entraid/applications/grant_site_selected_permission.py``.

Examples::

    python -m tests.setup
    python -m tests.setup --dry-run
    python -m tests.setup --sites selected --site https://contoso.sharepoint.com/sites/team
    python -m tests.setup --with-secret --new-app --app-name my-app
    python -m tests.setup -y --tenant contoso.onmicrosoft.com --client-id <app-id>
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

from tests.settings import FLOWS, settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = Path(__file__).resolve().parent
CERT_PUBLIC = TEST_DIR / "selfsigncert.crt"
CERT_PRIVATE = TEST_DIR / "selfsigncert.pem"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_BAK = PROJECT_ROOT / ".env.bak"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"

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
def _load_env_lines() -> list[str]:
    source = ENV_PATH if ENV_PATH.is_file() else ENV_EXAMPLE
    if not source.is_file():
        return []
    return source.read_text(encoding="utf-8-sig").splitlines()


def _read_env_values() -> dict[str, str]:
    values: dict[str, str] = {}
    if not ENV_PATH.is_file():
        return values
    for line in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        values[key.strip()] = value.strip().strip("'\"")
    return values


def merge_env(overrides: dict[str, str], defaults: dict[str, str]) -> str:
    """Return ``.env`` text with ``overrides`` applied and missing ``defaults`` filled.

    Comments and unrelated keys are preserved. ``overrides`` replace a value in
    place; ``defaults`` only fill an existing key when it is empty.
    """
    lines = _load_env_lines()
    pending = dict(overrides)
    fill = dict(defaults)
    output: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key, _, current = stripped.partition("=")
            key = key.strip()
            if key in pending:
                output.append(f"{key}={pending.pop(key)}")
                continue
            if key in fill:
                fallback = fill.pop(key)
                if not current.strip():
                    output.append(f"{key}={fallback}")
                    continue
        output.append(raw)
    tail: dict[str, str] = {}
    tail.update(fill)
    tail.update(pending)
    if tail:
        output.append("")
        output.append("# Added by python -m tests.setup")
        output.extend(f"{key}={value}" for key, value in tail.items())
    return "\n".join(output).rstrip() + "\n"


def _mask_secrets(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith(("OFFICE365_CLIENT_SECRET=", "OFFICE365_PASSWORD=")):
            lines.append(f"{line.split('=', 1)[0]}=<hidden>")
        else:
            lines.append(line)
    return "\n".join(lines)


def _env_updates(opts: _Options, target_id: str, thumbprint: str, secret_value: str) -> tuple[dict, dict]:
    overrides = {"OFFICE365_TENANT": opts.tenant, "OFFICE365_CLIENT_ID": target_id}
    if thumbprint:
        overrides["OFFICE365_CERT_THUMBPRINT"] = thumbprint
        overrides["OFFICE365_CERT_PATH"] = str(CERT_PRIVATE.relative_to(PROJECT_ROOT))
    if opts.admin:
        overrides["OFFICE365_ADMIN_USERNAME"] = opts.admin
    if opts.username:
        overrides["OFFICE365_USERNAME"] = opts.username
    if opts.username_alt:
        overrides["OFFICE365_USERNAME_ALT"] = opts.username_alt
    if opts.shared_mailbox:
        overrides["OFFICE365_SHARED_MAILBOX_UPN"] = opts.shared_mailbox
    if opts.password:
        overrides["OFFICE365_PASSWORD"] = opts.password
    if secret_value:
        overrides["OFFICE365_CLIENT_SECRET"] = secret_value

    defaults: dict[str, str] = {}
    prefix = _tenant_prefix(opts.tenant, opts.username)
    if prefix:
        base = f"https://{prefix}.sharepoint.com"
        defaults.update(
            {
                "OFFICE365_TENANT_PREFIX": prefix,
                "OFFICE365_ROOT_SITE_URL": base,
                "OFFICE365_SITE_URL": base,
                "OFFICE365_TEAM_SITE_URL": f"{base}/sites/team",
                "OFFICE365_ADMIN_SITE_URL": f"https://{prefix}-admin.sharepoint.com",
                "OFFICE365_CONTENT_TYPE_HUB_URL": f"{base}/sites/contentTypeHub",
            }
        )
    if opts.sites_scope == "selected" and opts.site_urls:
        defaults["OFFICE365_SITE_URL"] = opts.site_urls[0]
        defaults["OFFICE365_TEAM_SITE_URL"] = opts.site_urls[0]
    return overrides, defaults


def _write_env(opts: _Options, target_id: str, thumbprint: str, secret_value: str, *, dry_run: bool) -> None:
    overrides, defaults = _env_updates(opts, target_id, thumbprint, secret_value)
    text = merge_env(overrides, defaults)
    if dry_run:
        print("== .env (dry run; nothing written) ==")
        print(_mask_secrets(text))
        return
    if ENV_PATH.is_file():
        shutil.copy2(ENV_PATH, ENV_BAK)
    ENV_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {ENV_PATH.relative_to(PROJECT_ROOT)} (backup: {ENV_BAK.name})")
    if not secret_value:
        print(
            "Note: the 'app-only' (client secret) flow is not configured. Create one with\n"
            "      `python -m tests.setup --with-secret`, or "
            "examples/entraid/applications/rotate_secret.py."
        )
    print("Next: python -m tests.doctor")


def _print_readiness() -> None:
    ready = settings.readiness()
    width = max(len(flow.label) for flow in FLOWS.values())
    print("Auth readiness (environment + .env):")
    for flow, spec in FLOWS.items():
        missing = ready[flow]
        detail = "" if not missing else "  missing: " + ", ".join(missing)
        print(f"  {spec.label:<{width}}  {'ready' if not missing else 'not ready':<9}{detail}")
    print()


# --------------------------------------------------------------------------- #
# Options / Graph actions
# --------------------------------------------------------------------------- #
def _resolve_core(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[str, str, str]:
    tenant = args.tenant or settings.tenant
    if not tenant:
        if args.yes:
            parser.error("--tenant is required with --yes")
        tenant = _ask("Tenant (domain or id)")
    if not tenant:
        parser.error("--tenant is required")

    client_id = args.client_id or settings.client_id
    if not client_id:
        if args.yes:
            parser.error("--client-id is required with --yes")
        client_id = _ask("Sign-in app (client) ID")
    if not client_id:
        parser.error("--client-id is required")

    admin = args.admin or settings.admin_username
    if args.interactive and not admin and not args.yes:
        admin = _ask("Admin UPN (interactive sign-in)")
    if args.interactive and not admin:
        parser.error("--admin is required with --interactive")
    return tenant, client_id, admin


def _resolve_sites(args: argparse.Namespace) -> tuple[str, list[str]]:
    if args.site:
        return "selected", list(args.site)
    scope = args.sites or "all"
    if scope == "selected" and not args.yes:
        return scope, _ask_site_urls()
    return scope, []


def _resolve_extras(args: argparse.Namespace) -> bool:
    if args.pick_users or args.with_password:
        return True
    if args.username_alt is not None or args.shared_mailbox is not None:
        return True
    if args.yes:
        return False
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
    if args.with_secret:
        return True
    if args.yes:
        return False
    if existing_values.get("OFFICE365_CLIENT_SECRET") or settings.client_secret:
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
        app_name=args.app_name or DEFAULT_APP_NAME,
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
    try:
        return call()
    except Exception as exc:  # noqa: BLE001 - discovery is best-effort; the caller falls back
        message = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
        print(f"  (lookup skipped: {message})")
        return fallback


def _signed_in_upn(client: GraphClient) -> str:
    me = _try(lambda: client.me.get().execute_query(), None)
    if me is None:
        return ""
    return getattr(me, "user_principal_name", "") or ""


def _list_users(client: GraphClient) -> list[str]:
    users = _try(lambda: client.users.top(25).get().execute_query(), None)
    if users is None:
        return []
    upns: list[str] = []
    for user in users:
        upn = getattr(user, "user_principal_name", "") or ""
        if upn:
            upns.append(upn)
    return upns


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
        app = client.applications.ensure(opts.app_name, create_service_principal=True).execute_query()
        print(f"Created app '{app.display_name}' ({app.app_id})")
    else:
        app = client.applications.ensure(opts.app_name, opts.client_id, create_service_principal=True).execute_query()
    target_id = app.app_id

    display_name = getattr(app, "display_name", None) or opts.app_name
    thumbprint = _ensure_certificate(client, app, target_id, display_name, opts)
    secret_value = _ensure_secret(client, target_id, display_name, existing_values, opts)
    return target_id, thumbprint, secret_value


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate .env for local test/example authentication.")
    parser.add_argument("--tenant", help="tenant domain or id (prompted when missing)")
    parser.add_argument("--client-id", dest="client_id", help="app id used to sign in (and, by default, configure)")
    parser.add_argument("--admin", help="admin UPN (interactive sign-in and .env)")
    parser.add_argument("--interactive", action="store_true", help="browser sign-in instead of the device code flow")
    parser.add_argument("--new-app", action="store_true", help="create a new app registration")
    parser.add_argument("--app-name", help="display name for --new-app / certificate")
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
    existing_values = _read_env_values()
    opts = _resolve_options(args, parser, existing_values)

    _print_readiness()

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
        return 0

    client = _sign_in(opts)
    _apply_discovery(opts, _signed_in_upn(client))
    if opts.extras:
        _prompt_optional_users(client, opts)
    target_id, thumbprint, secret_value = _configure_credentials(client, opts, existing_values)
    _write_env(opts, target_id, thumbprint, secret_value, dry_run=False)
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        code = 130
    raise SystemExit(code)
