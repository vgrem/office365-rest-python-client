"""
Read a large list while pacing requests against SharePoint throttling signals.

SharePoint Online doesn't return IETF ``RateLimit-*`` headers; instead every
(successful) response carries ``X-SharePointHealthScore`` (lower = healthier)
and throttled responses add ``Retry-After``. ``throttle_guard`` parses whichever
of these are present after each request and calls ``pace``, so we back off
proactively instead of hammering an unhealthy server.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/how-to-avoid-getting-throttled-or-blocked-in-sharepoint-online
"""

import argparse
import time

from office365.runtime.http.throttling import ThrottleLimits, throttle_guard
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

HEALTH_BACKOFF = 6  # sleep when the server health score is this high or above (0 = healthiest)


def pace(limits: ThrottleLimits) -> None:
    """Called after every request inside the guard — honor server delays, back off when unhealthy."""
    print(
        f"  health={limits.health_score}, remaining={limits.remaining}, "
        f"reset={limits.reset}, retry_after={limits.retry_after}"
    )
    delay = limits.retry_after or limits.reset
    if delay:
        print(f"  server asked us to wait {delay}s")
        time.sleep(delay)
    elif limits.health_score is not None and limits.health_score >= HEALTH_BACKOFF:
        print(f"  health score {limits.health_score} — backing off")
        time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Read a large list while pacing against SharePoint throttling")
    parser.add_argument("--list-title", default="Contacts_Large")
    parser.add_argument("--select", default="Title,FullName,WorkCountry")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    # Every request inside the block is monitored; the guard detaches on exit.
    with throttle_guard(ctx, on_limits=pace):
        items = (
            ctx.web.lists.get_by_title(args.list_title).items.get_all().select(args.select.split(",")).execute_query()
        )

    print(f"\nRead {len(items)} items.")


if __name__ == "__main__":
    main()
