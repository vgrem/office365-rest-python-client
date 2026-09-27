#!/usr/bin/env python3
"""Print a short-lived GitHub App installation token for local ``gh`` usage.

``gh`` cannot authenticate as a GitHub App, so this signs a JWT with the app's
private key, exchanges it for an installation token and prints it. Export the
result to act as ``office365-maintainer[bot]``:

    export GH_TOKEN="$(uv run python scripts/github_app_token.py \
        --app-id 5098142 \
        --private-key ~/.config/office365-maintainer/app.pem \
        --repo vgrem/office365-rest-python-client)"
    gh issue comment 123 --body-file reply.md

The token expires after about an hour; re-run to refresh it. ``git`` operations
are unaffected and still use your own identity.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from base64 import urlsafe_b64encode
from typing import Any, Dict, List, Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_API_URL = "https://api.github.com"


def _b64(data: bytes) -> str:
    return urlsafe_b64encode(data).rstrip(b"=").decode()


def _app_jwt(app_id: str, key: rsa.RSAPrivateKey) -> str:
    now = int(time.time())
    header = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":")).encode())
    claims = _b64(
        json.dumps(
            {"iat": now - 60, "exp": now + 540, "iss": app_id},  # GitHub caps JWT lifetime at 10 min
            separators=(",", ":"),
        ).encode()
    )
    signature = key.sign(f"{header}.{claims}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{header}.{claims}.{_b64(signature)}"


def _api(method: str, path: str, token: str, body: Optional[Dict[str, Any]] = None) -> Any:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(_API_URL + path, data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as ex:
        detail = ex.read().decode("utf-8", "replace")
        raise SystemExit(f"GitHub API {method} {path} failed ({ex.code}): {detail}") from ex


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Print a GitHub App installation token.")
    parser.add_argument("--app-id", required=True, help="App ID or client ID")
    parser.add_argument("--private-key", required=True, help="path to the app private key (.pem)")
    parser.add_argument("--repo", required=True, help="owner/name the app is installed on")
    args = parser.parse_args(argv)

    with open(args.private_key, "rb") as stream:
        key = serialization.load_pem_private_key(stream.read(), password=None)
    if not isinstance(key, rsa.RSAPrivateKey):
        raise SystemExit(f"'{args.private_key}' is not an RSA private key")

    token = _app_jwt(args.app_id, key)
    owner = args.repo.split("/", 1)[0].lower()
    installations = _api("GET", "/app/installations", token)
    installation_id = next(
        (i["id"] for i in installations if (i.get("account") or {}).get("login", "").lower() == owner),
        None,
    )
    if installation_id is None:
        raise SystemExit(f"App is not installed on '{owner}'")
    print(_api("POST", f"/app/installations/{installation_id}/access_tokens", token, {})["token"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
