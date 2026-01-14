from office365.runtime.client_value import ClientValue


class RefinerEntry(ClientValue):
    def __init__(
        self,
        refinement_count: int = None,
        refinement_name: str = None,
        refinement_token: str = None,
        refinement_value: str = None,
    ):
        """
        :param int refinement_count:
        :param str refinement_name:
        """
        self.RefinementCount = refinement_count
        self.RefinementName = refinement_name
        self.RefinementToken = refinement_token
        self.RefinementValue = refinement_value

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.RefinerEntry"
