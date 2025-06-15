from enum import Enum


class HttpMethod(Enum):
    """Defines HTTP methods with auto-generated values matching standard method names.

    Usage:
        >>> HttpMethod.Get
        <HttpMethod.GET: 'GET'>
        >>> HttpMethod.Get.value
        'GET'
        >>> HttpMethod('GET')
        <HttpMethod.GET: 'GET'>
    """

    Get = "GET"
    Post = "POST"
    Patch = "PATCH"
    Delete = "DELETE"
    Put = "PUT"

    def __str__(self):
        return self.value
