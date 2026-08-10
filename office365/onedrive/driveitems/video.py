from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Video(ClientValue):
    audioBitsPerSample: int | None = None
    audioChannels: int | None = None
    audioFormat: str | None = None
    audioSamplesPerSecond: int | None = None
    bitrate: int | None = None
    duration: int | None = None
    fourCC: str | None = None
    frameRate: float | None = None
    height: int | None = None
    width: int | None = None
    "The Video resource groups video-related data items into a single structure."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Video"
