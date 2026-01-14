from office365.runtime.client_value import ClientValue


class ProfilePropertyViewEditPolicy(ClientValue):
    def __init__(
        self,
        is_disabled: bool = None,
        is_required: bool = None,
        is_taxonomic: bool = None,
        is_user_editable: bool = None,
        is_visible_on_editor: bool = None,
        privacy: int = None,
        user_override_privacy: bool = None,
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
