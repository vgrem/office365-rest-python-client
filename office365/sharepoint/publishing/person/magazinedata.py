from office365.runtime.client_value import ClientValue


class PersonMagazineData(ClientValue):

    def __init__(
        self,
        about_me: str = None,
        background_image_url: str = None,
        background_image_x: int = None,
        background_image_y: int = None,
        department_name: str = None,
        display_name: str = None,
        email: str = None,
        has_edit_permission: bool = None,
        office: str = None,
        phone: str = None,
        picture_url: str = None,
        title: str = None,
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
