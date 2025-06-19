from enum import Enum


class ListTemplateType(Enum):
    """Specifies the base list template type to use when creating a list."""

    genericList = "genericList"

    documentLibrary = "documentLibrary"

    survey = "survey"

    links = "links"

    announcements = "announcements"

    contacts = "contacts"

    events = "events"

    tasks = "tasks"

    discussionBoard = "discussionBoard"

    pictureLibrary = "pictureLibrary"

    dataSources = "dataSources"

    webTemplateCatalog = "webTemplateCatalog"

    userInformation = "userInformation"
