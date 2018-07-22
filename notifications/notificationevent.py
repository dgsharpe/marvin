from enum import Enum


class NotificationEventType(Enum):
    EMAIL_SENT = 1
    EMAIL_FAILURE = 2
    PUSHOVER_SENT = 3
    PUSHOVER_FAILURE = 4
    MATTERMOST_SENT = 5
    MATTERMOST_FAILURE = 6


class NotificationEvent:

    def __init__(self, event_type, event_message):
        self.eventType = event_type
        self.eventMessage = event_message
