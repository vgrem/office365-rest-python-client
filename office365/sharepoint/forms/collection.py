from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.forms.form import Form
from office365.sharepoint.pages.page_type import PageType


class FormCollection(EntityCollection[Form]):
    """Specifies a collection of list forms for a list."""

    def __init__(self, context, resource_path=None):
        """Specifies a collection of list forms for a list."""
        super().__init__(context, Form, resource_path)

    def get_by_id(self, id_: str):
        """Gets the form with the specified ID.

        :param str id_: Specifies the identifier of the list form.
        """
        return Form(
            self.context, ServiceOperationPath("GetById", [id_], self.resource_path)
        )

    def get_by_page_type(self, form_type: PageType) -> Form:
        """
        Returns the list form with the specified page type. If there is more than one list form with
        the specified page type, the protocol server MUST return one list form as determined by the protocol server.
        If there is no list form with the specified page type, the server MUST return NULL.

        :param str or office365.sharepoint.pages.page_type.PageType form_type: Specifies the page type of the list
            form to return. It MUST be DISPLAYFORM, EDITFORM or NEWFORM.
            Type: office365.sharepoint.pages.page_type.PageType
        """
        return Form(
            self.context,
            ServiceOperationPath(
                "GetByPageType", [form_type.value], self.resource_path
            ),
        )
