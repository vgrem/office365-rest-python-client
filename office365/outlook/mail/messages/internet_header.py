from __future__ import annotations

from office365.runtime.client_value import ClientValue


class InternetMessageHeader(ClientValue):
    """
    A key-value pair that represents an Internet message header, as defined by RFC5322, that provides details of the
    network path taken by a message from the sender to the recipient.
    """

    name: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InternetMessageHeader"
