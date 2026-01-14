"""
Acquire SharePoint Online browser-session cookies using Playwright and save them into
storage_state.json (or a custom path), which can be consumed by examples/sharepoint/auth_cookies.py.

Requirements (not installed by the library):
  pip install playwright
  playwright install chromium

Usage:
  SP_SITE_URL="https://contoso.sharepoint.com/sites/demo" \
  PLAYWRIGHT_STORAGE_STATE="./storage_state.json" \
  HEADLESS=false \
  python examples/sharepoint/auth/capture_cookies_with_playwright.py

Notes:
- The script opens a browser window. Complete the Microsoft login (including MFA) manually.
- After login, return to the terminal and press Enter to persist cookies.
- The resulting storage_state.json can be used by auth_cookies.py.
"""

import os

from playwright.sync_api import sync_playwright


def main() -> None:
    site_url = os.environ.get("SP_SITE_URL")
    if not site_url:
        raise SystemExit("SP_SITE_URL is required, e.g. https://contoso.sharepoint.com/sites/demo")

    storage_state_path = os.environ.get("PLAYWRIGHT_STORAGE_STATE", "./storage_state.json")
    headless_env = os.environ.get("HEADLESS", "false").lower()
    headless = headless_env in ("1", "true", "yes")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(site_url)
        # Wait for network to be idle; login flow may redirect to Microsoft login pages
        page.wait_for_load_state("networkidle")

        print("\nA browser window is open. Complete the login (including MFA) if prompted.")
        input("When the SharePoint page is fully loaded and you are authenticated, press Enter here to continue...")

        # Persist cookies and related state
        context.storage_state(path=storage_state_path)
        print(f"Saved Playwright storage state to: {storage_state_path}")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
