from office365.runtime.client_value import ClientValue


class RecentAndJoinedTeamsResponse(ClientValue):

    def __init__(self, joined_teams: str = None, joined_teams_error: int = None):
        self.joinedTeams = joined_teams
        self.joinedTeamsError = joined_teams_error

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.RecentAndJoinedTeamsResponse"
