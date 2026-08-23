from office365.entity_collection import EntityCollection
from office365.outlook.calendar.calendar import Calendar


class CalendarCollection(EntityCollection[Calendar]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, Calendar, resource_path)
