"""Download CSDL metadata from a live service into ``generator/metadata``.

Client libraries and credentials are only touched when :func:`fetch` runs, so the
rest of the generator never depends on them.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Optional
from xml.dom import minidom

METADATA_DIR = Path(__file__).parent

_ENV_NAMES = ("tenant", "client_id", "client_secret", "username", "password", "site_url")


def pretty_xml(content: bytes) -> str:
    """Indent raw CSDL bytes the way the committed snapshots are formatted."""
    return minidom.parseString(content.decode("utf-8")).toprettyxml(indent="   ")


def export_to_file(path: str | Path, content: bytes) -> None:
    Path(path).write_text(pretty_xml(content), encoding="utf-8")


def load_credentials() -> dict[str, str]:
    """Credentials from ``O365_<NAME>`` environment variables, else ``tests.settings``."""
    values = {name: os.environ.get(f"O365_{name.upper()}") for name in _ENV_NAMES}
    if all(values.values()):
        return values  # type: ignore[return-value]
    from tests import settings

    return {name: values[name] or getattr(settings, name, "") for name in _ENV_NAMES}  # type: ignore[misc]


def default_path(service: str, version: Optional[str]) -> Path:
    if service == "sharepoint":
        return METADATA_DIR / "SharePoint.xml"
    from office365.graph_version import GraphVersion

    beta = GraphVersion(version).is_beta if version else GraphVersion.default().is_beta
    return METADATA_DIR / ("GraphBeta.xml" if beta else "Graph.xml")


def _download(service: str, version: Optional[str], creds: dict[str, str]) -> bytes:
    if service == "sharepoint":
        from office365.sharepoint.client_context import ClientContext

        ctx = ClientContext(creds["site_url"]).with_username_and_password(
            creds["tenant"], creds["client_id"], creds["username"], creds["password"]
        )
        return ctx.get_metadata().execute_query().value
    from office365.graph_client import GraphClient
    from office365.graph_version import GraphVersion

    graph_version = GraphVersion(version) if version else GraphVersion.default()
    client = GraphClient(tenant=creds["tenant"], version=graph_version).with_client_secret(
        creds["client_id"], creds["client_secret"]
    )
    return client.get_metadata().execute_query().value


def fetch(
    service: str,
    version: Optional[str] = None,
    path: Optional[str] = None,
    *,
    downloader: Callable[[str, Optional[str], dict[str, Any]], bytes] = _download,
) -> Path:
    """Download the metadata of ``service`` and write it to ``path`` (or the default snapshot)."""
    target = Path(path) if path else default_path(service, version)
    content = downloader(service, version, load_credentials())
    export_to_file(target, content)
    return target
