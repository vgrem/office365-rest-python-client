from typing import Optional

from office365.runtime.client_value import ClientValue


class AmplifiedChannels(ClientValue):
    WasAmplifiedToEmail: Optional[bool] = None
    WasAmplifiedToSharePoint: Optional[bool] = None
    WasAmplifiedToTeams: Optional[bool] = None
    WasAmplifiedToVivaEngage: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifiedChannels"
