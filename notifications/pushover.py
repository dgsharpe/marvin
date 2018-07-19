from notifications.notification_client import NotificationClient
from notifications.notificationevent import NotificationEventType, NotificationEvent

import http.client, urllib

class Pushover(NotificationClient):
    NOTIFICATION_LOG_MESSAGE = "Pushover notification sent"
    NOTIFICATION_FAILED_LOG_MESSAGE = "Pushover notification failed to send"

    def __init__(self, config, pushover_app_token, pushover_user_key):
        super().__init__(config)
        self.pushover_app_token = pushover_app_token
        self.pushover_user_key = pushover_user_key

    def send_notification(self):
        log_lines = super().log_lines_since(self.NOTIFICATION_LOG_MESSAGE)
        if log_lines:
            return self.send_pushover(log_lines)

    def send_pushover(self, log_lines):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": self.pushover_app_token,
            "user": self.pushover_user_key,
            "message": log_lines,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        if conn.getresponse().status == 200:
            return NotificationEvent(NotificationEventType.PUSHOVER_SENT, self.NOTIFICATION_LOG_MESSAGE)
        else:
            return NotificationEvent(NotificationEventType.PUSHOVER_FAILURE, self.NOTIFICATION_FAILED_LOG_MESSAGE)
