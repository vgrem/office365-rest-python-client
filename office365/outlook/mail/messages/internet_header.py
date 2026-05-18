from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class InternetMessageHeader(ClientValue):
    """
    A key-value pair that represents an Internet message header, as defined by RFC5322, that provides details of the
    network path taken by a message from the sender to the recipient.
    """

    name: str | None = None
    value: str | None = None
