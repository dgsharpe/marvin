from enum import Enum


class NotificationEventType(Enum):
    EMAIL_SENT = 1
    EMAIL_FAILURE = 2
    PUSHOVER_SENT = 3
    PUSHOVER_FAILURE = 4


class NotificationEvent:

    def __init__(self, event_type):
        self.eventType = event_type
