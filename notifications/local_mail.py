from notifications.notification_client import NotificationClient
from notifications.notification_event import NotificationEventType, NotificationEvent
import subprocess

class LocalMail(NotificationClient):
    NOTIFICATION_TYPE = "Local mail"

    def __init__(self, config, local_mail_email_address):
        super().__init__(config)
        self.email_address = local_mail_email_address

    def send_notification(self):
        log_lines = super().log_lines_since_last_notification(self.NOTIFICATION_TYPE)
        if log_lines:
            return self.send_email(log_lines)

    def send_email(self, log_lines):
        try:
            process = subprocess.Popen(['mail', '-s', "Marvin log", self.email_address], stdin=subprocess.PIPE)
            process.communicate(log_lines.encode('utf-8'), 60)
            if process.returncode == 0:
                return NotificationEvent(NotificationEventType.LOCAL_MAIL_SENT, super().NOTIFICATION_LOG_MESSAGE + self.NOTIFICATION_TYPE)
            else:
                return NotificationEvent(NotificationEventType.LOCAL_MAIL_FAILURE, super().NOTIFICATION_FAILED_LOG_MESSAGE + self.NOTIFICATION_TYPE)
        except Exception as e:
            return NotificationEvent(NotificationEventType.LOCAL_MAIL_FAILURE, super().NOTIFICATION_FAILED_LOG_MESSAGE + self.NOTIFICATION_TYPE)