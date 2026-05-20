from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ItemPreviewInfo(ClientValue):
    """Contains information about how to embed a preview of a driveItem.

    Either getUrl, postUrl, or both may be returned depending on the current state of support for the specified options.

    postParameters is a string formatted as application/x-www-form-urlencoded,
    and if performing a POST to the postUrl the content-type should be set accordingly. For example:

    POST https://www.onedrive.com/embed_by_post
    Content-Type: application/x-www-form-urlencoded

    param1=value&param2=another%20value
    """

    getUrl: str | None = None
    postParameters: str | None = None
    postUrl: str | None = None
