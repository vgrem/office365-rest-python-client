from office365.runtime.client_value import ClientValue


class EnsureTeamForGroupExResponse(ClientValue):

    def __init__(self, teams_id: str = None, teams_url: str = None):
        self.teamsId = teams_id
        self.teamsUrl = teams_url
