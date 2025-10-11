from __future__ import annotations

from typing import Union

from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.contenttypes.content_type_id import ContentTypeId
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.lists.list import List


class DocumentSet(Folder):
    """Represents a set of documents."""

    @staticmethod
    def create(
        context: ClientContext,
        parent_folder: Folder,
        name: str,
        ct_id: Union[ContentTypeId, str] = "0x0120D520",
    ) -> DocumentSet:
        """
        Creates a DocumentSet (section 3.1.5.3) object on the server.

        :type context: office365.sharepoint.client_context.ClientContext
        :param office365.sharepoint.folders.folder.Folder parent_folder: The folder inside which to create the new
            DocumentSet.
        :param str name: The name to give to the new DocumentSet
        :param office365.sharepoint.contenttypes.content_type_id.ContentTypeId ct_id: The identifier of the content
            type to give to the new document set.
        """

        return_type = DocumentSet(context)
        parent_folder.folders.add_child(return_type)

        def _create(target_list: List) -> None:
            qry = ClientQuery(context, return_type=return_type)
            folder_url = parent_folder.server_relative_url + "/" + name
            return_type.set_property("ServerRelativeUrl", folder_url)

            def _construct_request(request: RequestOptions) -> None:
                list_name = target_list.title.replace(" ", "")
                request.url = rf"{context.base_url}/_vti_bin/listdata.svc/{list_name}"
                request.set_header("Slug", f"{folder_url}|{ct_id}")
                request.method = HttpMethod.Post

            context.add_query(qry).before_query_execute(_construct_request)

        def _parent_folder_loaded():
            custom_props = parent_folder.get_property("Properties")
            list_id = custom_props.get("vti_x005f_listname")
            target_list = context.web.lists.get_by_id(list_id)
            target_list.ensure_property("Title", _create, target_list=target_list)

        parent_folder.ensure_properties(["UniqueId", "Properties", "ServerRelativeUrl"], _parent_folder_loaded)
        return return_type

    @staticmethod
    def get_document_set(context: ClientContext, folder: Folder) -> DocumentSet:
        """Retrieves the document set object from a specified folder object.

        :type context: office365.sharepoint.client_context.ClientContext
        :param office365.sharepoint.folders.folder.Folder folder: the Folder object from which
            to get the document set
        """
        return_type = DocumentSet(context)
        return return_type
