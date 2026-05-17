from typing import Optional

from office365.runtime.client_value import ClientValue


class PersonMagazineData(ClientValue):
    def __init__(
        self,
        about_me: Optional[str] = None,
        background_image_url: Optional[str] = None,
        background_image_x: Optional[int] = None,
        background_image_y: Optional[int] = None,
        department_name: Optional[str] = None,
        display_name: Optional[str] = None,
        email: Optional[str] = None,
        has_edit_permission: Optional[bool] = None,
        office: Optional[str] = None,
        phone: Optional[str] = None,
        picture_url: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.AboutMe = about_me
        self.BackgroundImageUrl = background_image_url
        self.BackgroundImageX = background_image_x
        self.BackgroundImageY = background_image_y
        self.DepartmentName = department_name
        self.DisplayName = display_name
        self.Email = email
        self.HasEditPermission = has_edit_permission
        self.Office = office
        self.Phone = phone
        self.PictureUrl = picture_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineData"
