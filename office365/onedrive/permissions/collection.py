from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.permissions.permission import Permission
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    pass


class PermissionCollection(EntityCollection[Permission]):
    """Permission's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Permission, resource_path)

    def add(
        self,
        roles: list[str],
        identity: Entity | str | None = None,
        identity_type: str | None = None,
    ) -> Permission:
        """Create a new sharing permission.

        When ``identity`` is an :class:`Entity` (e.g. a loaded
        :class:`~office365.directory.serviceprincipals.ServicePrincipal`),
        its ``id`` and ``displayName`` are used directly and
        ``identity_type`` is inferred from the type.

        When ``identity`` is a ``str``, it must be the **object ID**
        of the target principal, and ``identity_type`` must be provided
        (e.g. ``"application"`` for a service principal).

        Args:
            roles: Permission roles (e.g. ``"read"``, ``"write"``).
            identity: The identity entity or its object ID.
            identity_type: Required when ``identity`` is a string.
                Ignored when ``identity`` is an Entity.

        Returns:
            The new :class:`Permission` (not yet executed).
        """

        return_type = Permission(self.context)
        self.add_child(return_type)

        if isinstance(identity, Entity):
            raw = type(identity).__name__.lower()
            identity_type = {"serviceprincipal": "application"}.get(raw, raw)

        def _add():
            payload = {
                "roles": roles,
                "grantedToIdentities": [
                    {
                        identity_type: Identity(
                            displayName=getattr(identity, "display_name", str(identity)),
                            id=getattr(identity, "id", str(identity)),
                        )
                    }
                ],
            }
            qry = CreateEntityQuery(self, payload, return_type)
            self.context.add_query(qry)

        if isinstance(identity, Entity):
            identity.ensure_properties(["displayName"]).after_execute(lambda _: _add())
        else:
            _add()
        return return_type

    def delete_all(self) -> Self:
        """Remove all access to resource"""

        def _delete(return_type: PermissionCollection) -> None:
            for permission in return_type:
                permission.delete_object()

        self.get_all().after_execute(_delete)
        return self
