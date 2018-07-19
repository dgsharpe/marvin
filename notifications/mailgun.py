from notifications.notification_client import NotificationClient
from notifications.notificationevent import NotificationEventType, NotificationEvent
import requests

class Mailgun(NotificationClient):
    NOTIFICATION_TYPE = "Mailgun"

    def __init__(self, config, mailgun_api_key, mailgun_domain_name, email_address):
        super().__init__(config)
        self.mailgun_api_key = mailgun_api_key
        self.mailgun_domain_name = mailgun_domain_name
        self.email_address = email_address

    def send_notification(self):
        log_lines = super().log_lines_since_last_notification(self.NOTIFICATION_TYPE)
        if log_lines:
            return self.send_email(log_lines)

    def send_email(self, log_lines):
        post_result = requests.post(
            "https://api.mailgun.net/v3/" + self.mailgun_domain_name + "/messages",
            auth=("api", self.mailgun_api_key),
            data={"from": "Marvin <mailgun@" + self.mailgun_domain_name + ">",
                  "to": [self.email_address],
                  "subject": "Marvin log",
                  "text": log_lines})
        if post_result.status_code == 200:
            return NotificationEvent(NotificationEventType.EMAIL_SENT, super().NOTIFICATION_LOG_MESSAGE + self.NOTIFICATION_TYPE)
        else:
            return NotificationEvent(NotificationEventType.EMAIL_FAILURE, super().NOTIFICATION_FAILED_LOG_MESSAGE + self.NOTIFICATION_TYPE)
