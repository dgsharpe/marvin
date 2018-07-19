import requests
import schedule
import threading
import time
import notificationevent

import http.client, urllib


class Notifications(threading.Thread):
    def __init__(self, config, event_queue):
        super(Notifications, self).__init__()
        self.config = config
        self.eventQueue = event_queue
        self.stop_request = threading.Event()

    def run(self):
        schedule.every(self.config.mailgun_frequency).minutes.do(self.send_email)
        while not self.stop_request.isSet():
            schedule.run_pending()
            time.sleep(1)

    def send_email(self):
        log_lines = ""
        for line in reversed(open(self.config.log_file_path).readlines()):
            if "Notification email sent" not in line:
                log_lines = line + log_lines
            else:
                break

        if log_lines and self.config.mailgun_enabled:
            post_result = requests.post(
                "https://api.mailgun.net/v3/" + self.config.mailgun_domain_name + "/messages",
                auth=("api", self.config.mailgun_api_key),
                data={"from": "Marvin <mailgun@" + self.config.mailgun_domain_name + ">",
                      "to": [self.config.email_address],
                      "subject": "Marvin log",
                      "text": log_lines})
            if post_result.status_code == 200:
                success_event = notificationevent.NotificationEventType.EMAIL_SENT
                self.eventQueue.put(notificationevent.NotificationEvent(success_event))
            else:
                fail_event = notificationevent.NotificationEventType.EMAIL_FAILURE
                self.eventQueue.put(notificationevent.NotificationEvent(fail_event))

    def send_pushover(self, log_lines):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": self.config.pushover_app_token,
            "user": self.config.pushover_user_key,
            "message": log_lines,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

    def send_email(self, log_lines):
        post_result = requests.post(
            "https://api.mailgun.net/v3/" + self.config.mailgun_domain_name + "/messages",
            auth=("api", self.config.mailgun_api_key),
            data={"from": "Marvin <mailgun@" + self.config.mailgun_domain_name + ">",
                  "to": [self.config.email_address],
                  "subject": "Marvin log",
                  "text": log_lines})
        if post_result.status_code == 200:
            success_event = notificationevent.NotificationEventType.EMAIL_SENT
            self.eventQueue.put(notificationevent.NotificationEvent(success_event))
        else:
            fail_event = notificationevent.NotificationEventType.EMAIL_FAILURE
            self.eventQueue.put(notificationevent.NotificationEvent(fail_event))

    def join(self, timeout=None):
        self.stop_request.set()
        super(Notifications, self).join(timeout)
