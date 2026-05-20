from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Audio(ClientValue):
    """
    The Audio resource groups audio-related properties on an item into a single structure.

    If a DriveItem has a non-null audio facet, the item represents an audio file.
    The properties of the Audio resource are populated by extracting metadata from the file.
    """

    album: str | None = None
    albumArtist: str | None = None
    artist: str | None = None
    bitrate: int | None = None
