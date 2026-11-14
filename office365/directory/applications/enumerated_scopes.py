from __future__ import annotations

from dataclasses import field

from office365.directory.applications.inheritable_scopes import InheritableScopes
from office365.runtime.types.collections import StringCollection


class EnumeratedScopes(InheritableScopes):
    scopes: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EnumeratedScopes"
