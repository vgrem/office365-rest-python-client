"""Guided local credential setup — run ``python -m tests.setup``.

Prompts for the minimum it needs (tenant, optional client secret, SharePoint
scope), reuses or creates a certificate and secret, then merges the values into
the repo-root ``.env``. Re-running is safe: existing credentials and ``.env``
entries are reused unless you ask for new ones.

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
"""

from __future__ import annotations

import argparse
import base64
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from office365.graph_client import GraphClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = Path(__file__).resolve().parent
CERT_PUBLIC = TEST_DIR / "selfsigncert.crt"
CERT_PRIVATE = TEST_DIR / "selfsigncert.pem"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_BAK = PROJECT_ROOT / ".env.bak"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"


@dataclass
class _Options:
    tenant: str
    client_id: str
    admin: str
    app_name: str
    want_secret: bool
    cert_choice: str
    sites_scope: str
    site_urls: list[str]
    create_new: bool
    force: bool
    rotate_secret: str | None


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


def _ask_choice(prompt: str, choices: list[str], default: str) -> str:
    options = "/".join(choices)
    while True:
        reply = input(f"{prompt} ({options}) [{default}]: ").strip().lower() or default
        if reply in choices:
            return reply
        print(f"Enter one of: {options}")


def _ask_site_urls() -> list[str]:
    print("Enter SharePoint site URLs (blank to finish):")
    urls: list[str] = []
    while True:
        value = input("  site URL: ").strip()
        if not value:
            return urls
        urls.append(value)


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
    result = subprocess.run(
        ["openssl", "x509", "-in", str(CERT_PUBLIC), "-noout", "-fingerprint", "-sha1"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().split("=", 1)[1].replace(":", "")


def _cert_thumbprint_b64() -> str:
    """The certificate thumbprint as Entra stores it in ``customKeyIdentifier``."""
    return base64.b64encode(bytes.fromhex(cert_thumbprint())).decode()


def _tenant_prefix(tenant: str) -> str:
    return tenant.split(".", maxsplit=1)[0] if "." in tenant else ""


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


def _apply_env(
    tenant: str,
    target_id: str,
    admin: str,
    thumbprint: str,
    secret_value: str,
    sites_scope: str,
    site_urls: list[str],
    *,
    dry_run: bool,
) -> None:
    overrides = {
        "OFFICE365_TENANT": tenant,
        "OFFICE365_CLIENT_ID": target_id,
        "OFFICE365_CERT_THUMBPRINT": thumbprint,
        "OFFICE365_CERT_PATH": str(CERT_PRIVATE.relative_to(PROJECT_ROOT)),
    }
    if admin:
        overrides["OFFICE365_ADMIN_USERNAME"] = admin
    if secret_value:
        overrides["OFFICE365_CLIENT_SECRET"] = secret_value

    defaults: dict[str, str] = {}
    prefix = _tenant_prefix(tenant)
    if prefix:
        defaults["OFFICE365_TENANT_PREFIX"] = prefix
        defaults["OFFICE365_ROOT_SITE_URL"] = f"https://{prefix}.sharepoint.com"
        defaults["OFFICE365_ADMIN_SITE_URL"] = f"https://{prefix}-admin.sharepoint.com"
    if sites_scope == "selected" and site_urls:
        defaults["OFFICE365_SITE_URL"] = site_urls[0]
        defaults["OFFICE365_TEAM_SITE_URL"] = site_urls[0]

    text = merge_env(overrides, defaults)
    if dry_run:
        print("== .env (dry run; nothing written) ==")
        print(text)
        return
    if ENV_PATH.is_file():
        shutil.copy2(ENV_PATH, ENV_BAK)
    ENV_PATH.write_text(text, encoding="utf-8")
    print(f"Updated {ENV_PATH.relative_to(PROJECT_ROOT)} (backup: {ENV_BAK.name})")
    print("Next: python -m tests.doctor")


# --------------------------------------------------------------------------- #
# Options / Graph actions
# --------------------------------------------------------------------------- #
def _resolve_secret_flag(args: argparse.Namespace) -> bool:
    if args.with_secret:
        return True
    if args.no_secret:
        return False
    if args.yes:
        return False
    return _ask_yes_no("Create a client secret?", default=False)


def _resolve_cert_choice(args: argparse.Namespace) -> str:
    local_exists = CERT_PUBLIC.is_file() and CERT_PRIVATE.is_file()
    if args.generate_cert:
        return "generate"
    if args.reuse_cert:
        return "reuse"
    if args.yes:
        return "reuse" if local_exists else "generate"
    return _ask_choice("Certificate", ["reuse", "generate"], "reuse" if local_exists else "generate")


def _resolve_sites_scope(args: argparse.Namespace) -> str:
    if args.sites:
        return args.sites
    if args.yes:
        return "all"
    return _ask_choice("SharePoint scope for .env", ["all", "selected"], "all")


def _resolve_options(args: argparse.Namespace, parser: argparse.ArgumentParser) -> _Options:
    tenant = args.tenant or ("" if args.yes else _ask("Tenant (domain or id)"))
    if not tenant:
        parser.error("--tenant is required (or run without --yes to be prompted)")
    client_id = args.client_id or ("" if args.yes else _ask("Sign-in app (client) ID"))
    if not client_id:
        parser.error("--client-id is required (or run without --yes to be prompted)")
    admin = args.admin or ("" if args.yes else _ask("Admin UPN (optional)"))
    if args.interactive and not admin:
        parser.error("--admin is required with --interactive")

    sites_scope = _resolve_sites_scope(args)
    site_urls = list(args.site)
    if sites_scope == "selected" and not site_urls and not args.yes:
        site_urls = _ask_site_urls()

    create_new = args.new_app or (not args.yes and _ask_yes_no("Create a new app registration?", default=False))
    return _Options(
        tenant=tenant,
        client_id=client_id,
        admin=admin,
        app_name=args.app_name or "office365-rest-python-client",
        want_secret=_resolve_secret_flag(args),
        cert_choice=_resolve_cert_choice(args),
        sites_scope=sites_scope,
        site_urls=site_urls,
        create_new=create_new,
        force=args.force,
        rotate_secret=args.rotate_secret,
    )


def _sign_in(args: argparse.Namespace, opts: _Options) -> GraphClient:
    client = GraphClient(tenant=opts.tenant)
    if args.interactive:
        client = client.with_token_interactive(opts.client_id, opts.admin)
    else:
        client = client.with_device_flow(opts.client_id)
    return client.require_role("Global Administrator", "Privileged Role Administrator")


def _ensure_certificate(client: GraphClient, app, target_id: str, display_name: str, opts: _Options) -> str:
    local_exists = CERT_PUBLIC.is_file() and CERT_PRIVATE.is_file()
    existing_keys = {key.customKeyIdentifier for key in app.key_credentials if key.customKeyIdentifier}
    local_thumb_b64 = _cert_thumbprint_b64() if local_exists else ""
    already_uploaded = bool(local_thumb_b64) and local_thumb_b64 in existing_keys

    if opts.cert_choice == "reuse" and local_exists and already_uploaded and not opts.force:
        print("Certificate already uploaded; reusing.")
        return cert_thumbprint()

    if opts.force or opts.cert_choice == "generate" or not local_exists:
        _require_openssl()
        generate_certificate(display_name)
        print(f"Generated {CERT_PUBLIC.relative_to(PROJECT_ROOT)}")
    else:
        print("Uploading the existing local certificate.")
    client.applications.get_by_app_id(target_id).add_certificate(CERT_PUBLIC.read_bytes(), display_name).execute_query()
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
        app = client.applications.add(opts.app_name, signInAudience="AzureADMyOrg").execute_query()
        target_id = app.app_id
        print(f"Created app '{app.display_name}' ({target_id})")
    else:
        target_id = opts.client_id
        app = client.applications.get_by_app_id(target_id).get().execute_query()

    display_name = getattr(app, "display_name", None) or opts.app_name
    thumbprint = _ensure_certificate(client, app, target_id, display_name, opts)
    secret_value = _ensure_secret(client, target_id, display_name, existing_values, opts)
    return target_id, thumbprint, secret_value


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Configure .env for local test/example authentication.")
    parser.add_argument("--tenant", help="tenant domain or id")
    parser.add_argument("--client-id", dest="client_id", help="app id used to sign in (and, by default, configure)")
    parser.add_argument("--admin", help="admin UPN (interactive sign-in and .env)")
    parser.add_argument("--interactive", action="store_true", help="browser sign-in instead of the device code flow")
    parser.add_argument("--new-app", action="store_true", help="create a new app registration")
    parser.add_argument("--app-name", help="display name for --new-app / certificate")
    parser.add_argument("--reuse-cert", action="store_true", help="keep the existing local certificate")
    parser.add_argument("--generate-cert", action="store_true", help="generate a new certificate")
    parser.add_argument("--force", action="store_true", help="regenerate and re-upload the certificate")
    parser.add_argument("--with-secret", action="store_true", help="create a client secret")
    parser.add_argument("--no-secret", action="store_true", help="do not create a client secret")
    parser.add_argument(
        "--rotate-secret", metavar="KEY_ID", help="delete this existing secret id before creating a new one"
    )
    parser.add_argument("--sites", choices=["all", "selected"], help="SharePoint scope written to .env")
    parser.add_argument("--site", action="append", default=[], metavar="URL", help="SharePoint site URL (repeatable)")
    parser.add_argument("--dry-run", action="store_true", help="preview the .env merge without signing in or writing")
    parser.add_argument("-y", "--yes", action="store_true", help="accept defaults; do not prompt")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    opts = _resolve_options(args, parser)
    existing_values = _read_env_values()

    if args.dry_run:
        target_id = "<new-app-id>" if opts.create_new else opts.client_id
        thumbprint = cert_thumbprint() if CERT_PUBLIC.is_file() else "<thumbprint>"
        if opts.want_secret:
            secret_value = existing_values.get("OFFICE365_CLIENT_SECRET") or "<created-at-setup>"
        else:
            secret_value = ""
        _apply_env(
            opts.tenant, target_id, opts.admin, thumbprint, secret_value, opts.sites_scope, opts.site_urls, dry_run=True
        )
        return 0

    client = _sign_in(args, opts)
    target_id, thumbprint, secret_value = _configure_credentials(client, opts, existing_values)
    _apply_env(
        opts.tenant,
        target_id,
        opts.admin,
        thumbprint,
        secret_value,
        opts.sites_scope,
        opts.site_urls,
        dry_run=False,
    )
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        code = 130
    raise SystemExit(code)
