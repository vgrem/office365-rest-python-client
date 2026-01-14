from office365.runtime.client_value import ClientValue


class SiteScriptActionStatus(ClientValue):
    def __init__(
        self,
        action_index: int = None,
        action_key: str = None,
        action_title: str = None,
        action_verb: str = None,
        last_modified: int = None,
        ordinal_index: int = None,
        outcome_code: int = None,
        outcome_text: str = None,
        site_script_id: str = None,
        site_script_index: int = None,
        site_script_title: str = None,
    ):
        self.ActionIndex = action_index
        self.ActionKey = action_key
        self.ActionTitle = action_title
        self.ActionVerb = action_verb
        self.LastModified = last_modified
        self.OrdinalIndex = ordinal_index
        self.OutcomeCode = outcome_code
        self.OutcomeText = outcome_text
        self.SiteScriptID = site_script_id
        self.SiteScriptIndex = site_script_index
        self.SiteScriptTitle = site_script_title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptActionStatus"
