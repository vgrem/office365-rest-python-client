from office365.entity import Entity


class RetentionEventType(Entity):
    """Represents a single group for the same type of retention events.

    When a retention event is created, it's associated with a specific event type that in turn is associated
    with a retention label. Only content with that retention label applied will be retained for the specified
    retention period. For details, see Start retention when an event occurs."""
