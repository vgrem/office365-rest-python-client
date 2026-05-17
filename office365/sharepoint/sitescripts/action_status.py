from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteScriptActionStatus(ClientValue):
    def __init__(
        self,
        action_index: Optional[int] = None,
        action_key: Optional[str] = None,
        action_title: Optional[str] = None,
        action_verb: Optional[str] = None,
        last_modified: Optional[int] = None,
        ordinal_index: Optional[int] = None,
        outcome_code: Optional[int] = None,
        outcome_text: Optional[str] = None,
        site_script_id: Optional[str] = None,
        site_script_index: Optional[int] = None,
        site_script_title: Optional[str] = None,
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
