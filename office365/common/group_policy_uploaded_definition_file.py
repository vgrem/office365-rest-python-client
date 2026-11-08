from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.common.group_policy_uploaded_definition_file_status import GroupPolicyUploadedDefinitionFileStatus
from office365.common.group_policy_uploaded_language_file import GroupPolicyUploadedLanguageFile
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_operation import GroupPolicyOperation


@version("beta")
class GroupPolicyUploadedDefinitionFile(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[bytes]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="defaultLanguageCode")
    @property
    def default_language_code(self) -> Optional[str]:
        """Gets the defaultLanguageCode property"""
        return self.properties.get("defaultLanguageCode", None)

    @odata(name="groupPolicyUploadedLanguageFiles")
    @property
    def group_policy_uploaded_language_files(self) -> ClientValueCollection[GroupPolicyUploadedLanguageFile]:
        """Gets the groupPolicyUploadedLanguageFiles property"""
        return self.properties.get(
            "groupPolicyUploadedLanguageFiles",
            ClientValueCollection[GroupPolicyUploadedLanguageFile](GroupPolicyUploadedLanguageFile),
        )

    @odata(name="status")
    @property
    def status(self) -> Optional[GroupPolicyUploadedDefinitionFileStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="uploadDateTime")
    @property
    def upload_date_time(self) -> Optional[datetime]:
        """Gets the uploadDateTime property"""
        return self.properties.get("uploadDateTime", None)

    @odata(name="groupPolicyOperations", navigation=True)
    @property
    def group_policy_operations(self) -> EntityCollection[GroupPolicyOperation]:
        """Gets the groupPolicyOperations property"""
        from office365.common.group_policy_operation import GroupPolicyOperation

        return self.properties.get(
            "groupPolicyOperations",
            EntityCollection[GroupPolicyOperation](
                self.context, GroupPolicyOperation, ResourcePath("groupPolicyOperations", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyUploadedDefinitionFile"

    def remove(self) -> Self:
        """remove operation."""
        qry = ServiceOperationQuery(self, "remove", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def add_language_files(
        self, group_policy_uploaded_language_files: ClientValueCollection[GroupPolicyUploadedLanguageFile]
    ) -> Self:
        """addLanguageFiles operation.

        Args:
            group_policy_uploaded_language_files (ClientValueCollection[GroupPolicyUploadedLanguageFile]):
                groupPolicyUploadedLanguageFiles parameter
        """
        qry = ServiceOperationQuery(
            self,
            "addLanguageFiles",
            None,
            {"groupPolicyUploadedLanguageFiles": group_policy_uploaded_language_files},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def remove_language_files(
        self, group_policy_uploaded_language_files: ClientValueCollection[GroupPolicyUploadedLanguageFile]
    ) -> Self:
        """removeLanguageFiles operation.

        Args:
            group_policy_uploaded_language_files (ClientValueCollection[GroupPolicyUploadedLanguageFile]):
                groupPolicyUploadedLanguageFiles parameter
        """
        qry = ServiceOperationQuery(
            self,
            "removeLanguageFiles",
            None,
            {"groupPolicyUploadedLanguageFiles": group_policy_uploaded_language_files},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def update_language_files(
        self, group_policy_uploaded_language_files: ClientValueCollection[GroupPolicyUploadedLanguageFile]
    ) -> Self:
        """updateLanguageFiles operation.

        Args:
            group_policy_uploaded_language_files (ClientValueCollection[GroupPolicyUploadedLanguageFile]):
                groupPolicyUploadedLanguageFiles parameter
        """
        qry = ServiceOperationQuery(
            self,
            "updateLanguageFiles",
            None,
            {"groupPolicyUploadedLanguageFiles": group_policy_uploaded_language_files},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def upload_new_version(
        self,
        content: bytes,
        group_policy_uploaded_language_files: ClientValueCollection[GroupPolicyUploadedLanguageFile],
    ) -> Self:
        """uploadNewVersion operation.

        Args:
            content (bytes):
                content parameter
            group_policy_uploaded_language_files (ClientValueCollection[GroupPolicyUploadedLanguageFile]):
                groupPolicyUploadedLanguageFiles parameter
        """
        qry = ServiceOperationQuery(
            self,
            "uploadNewVersion",
            None,
            {"content": content, "groupPolicyUploadedLanguageFiles": group_policy_uploaded_language_files},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
