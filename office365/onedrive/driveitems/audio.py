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
    composers: str | None = None
    copyright: str | None = None
    duration: int | None = None
    genre: str | None = None
    hasDrm: bool | None = None
    isVariableBitrate: bool | None = None
    title: str | None = None
    track: int | None = None
    trackCount: int | None = None
    year: int | None = None
    disc: int | None = None
    discCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Audio"
