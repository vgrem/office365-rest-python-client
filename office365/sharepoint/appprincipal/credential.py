from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class AppPrincipalCredential(Entity):
    """Represents a credential belonging to an app principal."""

    @staticmethod
    def create_from_symmetric_key(context, symmetric_key, not_before, not_after=None):
        """Create an instance of SP.AppPrincipalCredential that wraps a symmetric key.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            symmetric_key (str): The symmetric key of the app principal credential.
            not_before (datetime.datetime): The earliest time when the key is valid.
            not_after (datetime.datetime): The time when the key expires.
        """
        return_type = AppPrincipalCredential(context)
        payload = {
            "symmetricKey": symmetric_key,
            "notBefore": not_before.isoformat(),
            "notAfter": not_after.isoformat() if not_after else None,
        }
        qry = ServiceOperationQuery(return_type, "CreateFromSymmetricKey", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def create_from_key_group(context, key_group_identifier):
        """Create an instance of SP.AppPrincipalCredential that wraps a key group identifier.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            key_group_identifier (str): The key group identifier.
        """
        return_type = AppPrincipalCredential(context)
        payload = {"keyGroupIdentifier": key_group_identifier}
        qry = ServiceOperationQuery(return_type, "CreateFromKeyGroup", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type
