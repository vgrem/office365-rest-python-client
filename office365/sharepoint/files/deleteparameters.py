from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileDeleteParameters(ClientValue):
    bypass_checked_out: bool | None = None
    bypass_shared_lock: bool | None = None
    e_tag_match: str | None = None
