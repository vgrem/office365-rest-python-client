from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ProfilePropertyViewEditPolicy(ClientValue):
    IsDisabled: Optional[bool] = None
    IsRequired: Optional[bool] = None
    IsTaxonomic: Optional[bool] = None
    IsUserEditable: Optional[bool] = None
    IsVisibleOnEditor: Optional[bool] = None
    Privacy: Optional[int] = None
    UserOverridePrivacy: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfilePropertyViewEditPolicy"
