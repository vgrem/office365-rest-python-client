from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.scope_base import ScopeBase


@dataclass
class UserScope(ScopeBase):
    pass
