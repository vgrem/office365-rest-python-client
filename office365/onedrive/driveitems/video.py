from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Video(ClientValue):
    """The Video resource groups video-related data items into a single structure."""
