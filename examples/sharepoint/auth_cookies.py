import json
import os
from typing import Dict

from office365.sharepoint.client_context import ClientContext


def load_cookies_from_storage_state(path: str) -> Dict[str, str]:
    """Load cookies exported by Playwright storage_state.json and extract SPO cookies.

    The library does not depend on Playwright; this is a helper to demonstrate usage.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cookies = {}
    for c in data.get("cookies", []):
        name = c.get("name")
        if name in {"FedAuth", "rtFa", "SPOIDCRL"}:
            cookies[name] = c.get("value", "")
    return cookies


if __name__ == "__main__":
    site_url = os.environ.get(
        "SP_SITE_URL", "https://contoso.sharepoint.com/sites/demo"
    )
    storage_state_path = os.environ.get(
        "PLAYWRIGHT_STORAGE_STATE", "./storage_state.json"
    )

    def cookie_source():
        return load_cookies_from_storage_state(storage_state_path)

    ctx = ClientContext(site_url).with_cookies(cookie_source)
    web = ctx.web.get().execute_query()
    print(f"Web title: {web.title}")
