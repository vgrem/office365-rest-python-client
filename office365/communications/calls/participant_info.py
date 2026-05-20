from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ParticipantInfo(ClientValue):
    """Contains additional properties about the participant identity

    Fields:
        countryCode: The ISO 3166-1 Alpha-2 country code of the participant's best estimated physical
            location at the start of the call.
    """

    countryCode: str | None = None
