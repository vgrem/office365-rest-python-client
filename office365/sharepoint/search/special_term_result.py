from office365.runtime.client_value import ClientValue


class SpecialTermResult(ClientValue):

    def __init__(
        self,
        description: str = None,
        is_visual_best_bet: bool = None,
        pi_search_result_id: str = None,
        render_template_id: str = None,
        title: str = None,
        url: str = None,
    ):
        self.Description = description
        self.IsVisualBestBet = is_visual_best_bet
        self.PiSearchResultId = pi_search_result_id
        self.RenderTemplateId = render_template_id
        self.Title = title
        self.Url = url

    "Represents a row in the Table property of a SpecialTermResults Table"

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SpecialTermResult"
