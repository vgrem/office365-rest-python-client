from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Hashes(ClientValue):
    crc32Hash: str | None = None
    quickXorHash: str | None = None
    sha1Hash: str | None = None
    sha256Hash: str | None = None
    "The Hashes resource groups available hashes into a single structure for an item."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Hashes"
