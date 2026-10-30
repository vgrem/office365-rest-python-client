from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.externalconnectors.connectionoperationstatus import (
    ConnectionOperationStatus,
)
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.public_error import PublicError


class ConnectionOperation(PollableOperation, Entity):
    @odata(name="status")
    @property
    def status(self) -> ConnectionOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", ConnectionOperationStatus.unspecified)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ConnectionOperation"

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        from office365.runtime.types.public_error import PublicError

        return self.properties.get("error", PublicError())
