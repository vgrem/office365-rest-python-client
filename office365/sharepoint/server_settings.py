from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.sites.language_collection import LanguageCollection


class ServerSettings(Entity):
    """Provides methods for obtaining server properties."""

    def __init__(self, context):
        super().__init__(context, StaticPath("SP.ServerSettings"))

    @staticmethod
    def is_sharepoint_online(context) -> ClientResult[bool]:
        """
        :type context: office365.sharepoint.client_context.ClientContext
        """
        binding_type = ServerSettings(context)
        return_type = ClientResult(context)
        qry = ServiceOperationQuery(binding_type, "IsSharePointOnline", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_blocked_file_extensions(context) -> ClientResult[StringCollection]:
        """
        :type context: office365.sharepoint.client_context.ClientContext
        """
        binding_type = ServerSettings(context)
        return_type = ClientResult(context, StringCollection())
        qry = ServiceOperationQuery(
            binding_type,
            "GetBlockedFileExtensions",
            None,
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_global_installed_languages(context, compatibility_level: int) -> LanguageCollection:
        """
        Gets a list of installed languages that are compatible with a given version of SharePoint.

        :type context: office365.sharepoint.client_context.ClientContext
        :param int compatibility_level: The value of the major SharePoint version to query for installed languages.
        """
        binding_type = ServerSettings(context)
        return_type = LanguageCollection(context)
        qry = ServiceOperationQuery(
            binding_type,
            "GetGlobalInstalledLanguages",
            [compatibility_level],
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type
