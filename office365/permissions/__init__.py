"""What a call needs from a tenant, declared beside the request and checked by one type.

Five questions, one package:

:mod:`~office365.permissions.declaration`
    What a *model method* needs - ``@require_permission`` beside the request it builds, read
    back with :func:`~office365.permissions.declaration.declared` without calling the method.
:mod:`~office365.permissions.requirement`
    What a *caller* needs - one :class:`~office365.permissions.requirement.Requirement` per
    flow, joinable across calls, checked against a tenant's facts. A live test and a model
    method state the same fact with the same type.
:mod:`~office365.permissions.catalog`
    What an *API* publishes - the names a declaration may use, generated from the API's own
    service principal and committed, so a wrong name fails offline instead of looking like a
    grant the tenant never gave.
:mod:`~office365.permissions.index`
    What a *package* has - every operation that issues a request or names a permission,
    answered from source, so "which requests still name nothing" is a number, not a rumour.
:mod:`~office365.permissions.token`
    What a *token* proves - the audience it was issued for and the names it carries, read from
    the token itself, so a caller that has one needs no directory lookup at all.

A permission name only means something next to the API that defines it, so every declaration and
every requirement names its :class:`~office365.permissions.resource.ResourceName`; two APIs' names
are never merged into one requirement.

Nothing here sends a request, and nothing here reads a tenant: the probe that does lives with
the caller that owns a client. A token is the one exception to "a tenant is asked": its claims
are read where it already is, and its signature is never checked.

Graph's own permissions *entities* - ``identity``, ``identitySet``, ``resourceSpecificPermissionGrant``
- are model types and stay in :mod:`office365.directory.permissions`, where the metadata puts
them. This package is the vocabulary a caller uses, not a service namespace.
"""

from office365.permissions.catalog import APPLICATION, DELEGATED, Catalog, catalog, catalog_resources
from office365.permissions.declaration import PermissionRequirement, declared, derived_from, require_permission
from office365.permissions.index import Index, Operation, index
from office365.permissions.requirement import FLOWS, Requirement, TenantFacts
from office365.permissions.resource import ResourceName
from office365.permissions.roles import DirectoryRole
from office365.permissions.token import TokenClaims

__all__ = [
    "APPLICATION",
    "DELEGATED",
    "FLOWS",
    "Catalog",
    "DirectoryRole",
    "Index",
    "Operation",
    "PermissionRequirement",
    "Requirement",
    "ResourceName",
    "TenantFacts",
    "TokenClaims",
    "catalog",
    "catalog_resources",
    "declared",
    "derived_from",
    "index",
    "require_permission",
]

#: The permission catalog: it names what products require, it is not one.
__product__ = ""
