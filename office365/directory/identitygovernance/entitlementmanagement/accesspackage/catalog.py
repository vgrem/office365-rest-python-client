from office365.entity import Entity


class AccessPackageCatalog(Entity):
    """In Microsoft Entra entitlement management, an access package catalog is a container for zero or more access
    packages. Microsoft Entra entitlement management includes a built-in catalog named General.

     An access package catalog might also have linked resources that are used in those access packages
     to provide access. To view or change the membership of catalog-scoped roles, use the role assignments API
     with the entitlement management RBAC provider.
    """
