from __future__ import annotations

from office365.directory.applications.roles.role import AppRole
from office365.runtime.client_value_collection import ClientValueCollection


class AppRoleCollection(ClientValueCollection[AppRole]):
    """"""

    def __init__(self, initial_values=None):
        super().__init__(AppRole, initial_values)

    def get_by_value(self, value: str) -> AppRole | None:
        return next(iter([item for item in self._data if item.value == value]), None)

    def __getitem__(self, key: int | str) -> AppRole:
        if isinstance(key, str):
            item = self.get_by_value(key)
            if item is None:
                raise KeyError(key)
            return item
        return super().__getitem__(key)
