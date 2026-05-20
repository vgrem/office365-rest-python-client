from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SystemFacet(ClientValue):
    """
    The System facet indicates that the object is managed by the system for its own operation.
    Most apps should ignore items that have a System facet.
    """
