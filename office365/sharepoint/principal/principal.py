from typing import Optional

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity import Entity
from office365.sharepoint.principal.type import PrincipalType


class Principal(Entity):
    """Represents a user or group that can be assigned permissions to control security."""

    def __str__(self):
        return self.title or self.entity_type_name

    def __repr__(self):
        return self.user_principal_name or self.login_name or self.id or self.entity_type_name

    @property
    def id(self) -> Optional[int]:
        """Gets a value that specifies the member identifier for the user or group."""
        return self.properties.get("Id", None)

    @property
    def title(self) -> Optional[str]:
        """Gets a value that specifies the name of the principal."""
        return self.properties.get("Title", None)

    @title.setter
    def title(self, value: str) -> None:
        """Sets a value that specifies the name of the principal."""
        self.set_property("Title", value)

    @property
    def login_name(self) -> Optional[str]:
        """Gets the login name of the principal."""
        return self.properties.get("LoginName", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the UPN of the principal."""
        return self.properties.get("UserPrincipalName", None)

    @property
    def is_hidden_in_ui(self) -> Optional[bool]:
        """Gets the login name of the principal."""
        return self.properties.get("IsHiddenInUI", None)

    @property
    def principal_type(self) -> Optional[PrincipalType]:
        """Gets the type of the principal."""
        return self.properties.get("PrincipalType", PrincipalType.None_)

    @property
    def principal_type_name(self) -> str:
        return self.principal_type.name

    @property
    def property_ref_name(self):
        return "Id"

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "PrincipalType": self.principal_type,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super(Principal, self).set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if self._resource_path is None:
            if name == "LoginName":
                self._resource_path = ServiceOperationPath("GetByName", [value], self.parent_collection.resource_path)
        return self
