from office365.runtime.client_value import ClientValue


class SiteScriptActionResult(ClientValue):
    def __init__(
        self,
        outcome_text=None,
        target=None,
        error_code: int = None,
        outcome: int = None,
        target_id: str = None,
        title: str = None,
        verb: str = None,
    ):
        """
        :param str outcome_text:
        :param str target:
        """
        self.OutcomeText = outcome_text
        self.Target = target
        self.ErrorCode = error_code
        self.Outcome = outcome
        self.TargetId = target_id
        self.Title = title
        self.Verb = verb

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptActionResult"
