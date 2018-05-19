from enum import Enum


class NotificationEventType(Enum):
    EMAIL_SENT = 1
    EMAIL_FAILURE = 2


class NotificationEvent:

    def __init__(self, event_type):
        self.eventType = event_type
