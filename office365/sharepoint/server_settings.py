from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity
from office365.sharepoint.sites.language_collection import LanguageCollection


class ServerSettings(Entity):
    """Provides methods for obtaining server properties."""

    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("SP.ServerSettings")
        return self._resource_path

    @staticmethod
    def is_sharepoint_online(context: ClientContext) -> ClientResult[bool]:
        binding_type = ServerSettings(context)
        return_type = ClientResult(context)
        qry = ServiceOperationQuery(binding_type, "IsSharePointOnline", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_blocked_file_extensions(context: ClientContext) -> ClientResult[StringCollection]:
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
    def get_global_installed_languages(context: ClientContext, compatibility_level: int) -> LanguageCollection:
        """Gets a list of installed languages that are compatible with a given version of SharePoint."""
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
