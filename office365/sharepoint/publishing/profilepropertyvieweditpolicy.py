from typing import Optional

from office365.runtime.client_value import ClientValue


class ProfilePropertyViewEditPolicy(ClientValue):
    def __init__(
        self,
        is_disabled: Optional[bool] = None,
        is_required: Optional[bool] = None,
        is_taxonomic: Optional[bool] = None,
        is_user_editable: Optional[bool] = None,
        is_visible_on_editor: Optional[bool] = None,
        privacy: Optional[int] = None,
        user_override_privacy: Optional[bool] = None,
    ):
        self.IsDisabled = is_disabled
        self.IsRequired = is_required
        self.IsTaxonomic = is_taxonomic
        self.IsUserEditable = is_user_editable
        self.IsVisibleOnEditor = is_visible_on_editor
        self.Privacy = privacy
        self.UserOverridePrivacy = user_override_privacy

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfilePropertyViewEditPolicy"
