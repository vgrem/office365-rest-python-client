class RenderListDataOptions:
    """The type of data to return when rendering a list view as JSON."""

    """Default render type."""
    None_ = 0

    """ Returns the list data context information. """
    ContextInfo = 1

    """ Returns the list data. """
    ListData = 2

    """ Returns the list schema. """
    ListSchema = 4

    """ Returns the menu view of the list. """
    MenuView = 8
