"""Read a SharePoint site and its document libraries (your first call).

The smallest end-to-end app-only example: connect with the certificate created
by ``setup_sharepoint_app.py``, read the web properties, and list the document
libraries on the site.

Run ``setup_sharepoint_app.py`` once first: it creates the certificate, grants
``Sites.Selected`` and site access, and writes the values ``.env`` reads.
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main() -> None:
    ctx = ClientContext(site_url).with_client_certificate(
        tenant=tenant,
        client_id=client_id,
        thumbprint=cert_thumbprint,
        cert_path=cert_path,
    )

    web = ctx.web.get().execute_query()
    print(f"Connected to {web.title} ({web.url})")

    libraries = ctx.web.lists.get().execute_query()
    for library in libraries:
        print(f"  {library.title} (items: {library.item_count})")


if __name__ == "__main__":
    main()
