from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Bundle(ClientValue):
    """A bundle is a logical grouping of files used to share multiple files at once.
    It is represented by a driveItem entity containing a bundle facet and can be shared in the same way
    as any other driveItem."""

    album: str | None = None
    childCount: int | None = None
