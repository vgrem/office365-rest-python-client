from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PersonMagazineData(ClientValue):
    AboutMe: Optional[str] = None
    BackgroundImageUrl: Optional[str] = None
    BackgroundImageX: Optional[int] = None
    BackgroundImageY: Optional[int] = None
    DepartmentName: Optional[str] = None
    DisplayName: Optional[str] = None
    Email: Optional[str] = None
    HasEditPermission: Optional[bool] = None
    Office: Optional[str] = None
    Phone: Optional[str] = None
    PictureUrl: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineData"
