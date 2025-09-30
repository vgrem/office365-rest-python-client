from office365.runtime.client_value import ClientValue


class AmplifiedChannels(ClientValue):

    def __init__(
        self,
        was_amplified_to_email: bool = None,
        was_amplified_to_share_point: bool = None,
        was_amplified_to_teams: bool = None,
        was_amplified_to_viva_engage: bool = None,
    ):
        self.WasAmplifiedToEmail = was_amplified_to_email
        self.WasAmplifiedToSharePoint = was_amplified_to_share_point
        self.WasAmplifiedToTeams = was_amplified_to_teams
        self.WasAmplifiedToVivaEngage = was_amplified_to_viva_engage
