"""What a call needs from a tenant, declared beside the request and checked by one type.

Three questions, one package:

:mod:`~office365.permissions.declaration`
    What a *model method* needs - ``@require_permission`` beside the request it builds, read
    back with :func:`~office365.permissions.declaration.declared` without calling the method.
:mod:`~office365.permissions.requirement`
    What a *caller* needs - one :class:`~office365.permissions.requirement.Requirement` per
    flow, joinable across calls, checked against a tenant's facts. A live test and a model
    method state the same fact with the same type.
:mod:`~office365.permissions.index`
    What a *package* has - every operation that issues a request or names a permission,
    answered from source, so "which requests still name nothing" is a number, not a rumour.

A permission name only means something next to the API that defines it, so every declaration and
every requirement names its :class:`~office365.permissions.resource.ResourceName`; two APIs' names
are never merged into one requirement.

Nothing here sends a request, and nothing here reads a tenant: the probe that does lives with
the caller that owns a client.

Graph's own permissions *entities* - ``identity``, ``identitySet``, ``resourceSpecificPermissionGrant``
- are model types and stay in :mod:`office365.directory.permissions`, where the metadata puts
them. This package is the vocabulary a caller uses, not a service namespace.
"""

from office365.permissions.declaration import PermissionRequirement, declared, require_permission
from office365.permissions.index import Index, Operation, index
from office365.permissions.requirement import FLOWS, Requirement, TenantFacts
from office365.permissions.resource import ResourceName

__all__ = [
    "FLOWS",
    "Index",
    "Operation",
    "PermissionRequirement",
    "Requirement",
    "ResourceName",
    "TenantFacts",
    "declared",
    "index",
    "require_permission",
]
