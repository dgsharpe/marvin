from notifications.notification_client import NotificationClient
from notifications.notificationevent import NotificationEventType, NotificationEvent
import requests

class Mattermost(NotificationClient):
    NOTIFICATION_TYPE = "Mattermost"

    def __init__(self, config, mattermost_api_key, mattermost_url):
        super().__init__(config)
        self.mattermost_api_key = mattermost_api_key
        self.mattermost_url = mattermost_url

    def send_notification(self):
        log_lines = super().log_lines_since_last_notification(self.NOTIFICATION_TYPE)
        if log_lines:
            return self.send_mattermost(log_lines)

    def send_mattermost(self, log_lines):
        headers = {'Content-Type': 'application/json'}
        full_mattermost_url = self.mattermost_url + "/hooks/" + self.mattermost_api_key
        data = '{"text": "' + log_lines + '"}'
        post_result = requests.post(full_mattermost_url, headers=headers, data=data)
        if post_result.status_code == 200:
            return NotificationEvent(NotificationEventType.MATTERMOST_SENT, super().NOTIFICATION_LOG_MESSAGE + self.NOTIFICATION_TYPE)
        else:
            return NotificationEvent(NotificationEventType.MATTERMOST_FAILURE, super().NOTIFICATION_FAILED_LOG_MESSAGE + self.NOTIFICATION_TYPE)
