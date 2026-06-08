from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class ProfileImageStore(Entity):
    """The ProfileImageStore class specifies the user profile and service context."""

    def __init__(self, context):
        super().__init__(context, ResourcePath("SP.UserProfiles.ProfileImageStore"))

    def save_uploaded_file(
        self,
        profile_type,
        file_name_prefix,
        is_feed_attachment,
        client_file_path,
        file_size,
        file_stream,
    ):
        """The SaveUploadedFile method saves an uploaded file as a profile image. This method returns an array of URLs
        that provide access to the saved profile image.

        Args:
            profile_type (int): Specifies the profile type.
            file_name_prefix (str): Specifies a prefix for the name of the saved file.
            is_feed_attachment (bool): Has a true value if the file is being attached to a feed and, otherwise, has a false value.
            client_file_path (str): Specifies the path of the file on the client system.
            file_size (int): Specifies the size of the file in bytes.
            file_stream (str): Specifies a stream to read the file.
        """
        payload = {
            "profileType": profile_type,
            "fileNamePrefix": file_name_prefix,
            "isFeedAttachment": is_feed_attachment,
            "clientFilePath": client_file_path,
            "fileSize": file_size,
            "fileStream": file_stream,
        }
        return_type = ClientResult(self.context, StringCollection())
        qry = ServiceOperationQuery(self, "SaveUploadedFile", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.ProfileImageStore"
