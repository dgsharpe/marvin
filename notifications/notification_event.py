from enum import Enum


class NotificationEventType(Enum):
    MAILGUN__SENT = 1
    MAILGUN_FAILURE = 2
    PUSHOVER_SENT = 3
    PUSHOVER_FAILURE = 4
    LOCAL_MAIL_SENT = 5
    LOCAL_MAIL_FAILURE = 6


class NotificationEvent:
    def __init__(self, event_type, event_message):
        self.event_type = event_type
        self.event_message = event_message
