from typing import TypeVar

from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection

T = TypeVar("T", bound=ClientObject)


class TaxonomyItemCollection(ClientObjectCollection[T]):
    pass
