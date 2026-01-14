from office365.runtime.client_object import ClientObject


class NotFoundException(Exception):
    def __init__(self, entity=None, query=None):
        # type: (ClientObject, str) -> None
        self.entity = entity
        self.query = query

    def __str__(self):
        if self.entity is None:
            message = "Entity not found"
        else:
            message = f"{self.entity.entity_type_name} not found"

        if self.query is not None:
            message = f"{message} for query: {self.query}"
        return message
