import schedule
import threading
import time
import notifications.notification_event


class Notifications(threading.Thread):
    def __init__(self, config, event_queue):
        super(Notifications, self).__init__()
        self.config = config
        self.event_queue = event_queue
        self.stop_request = threading.Event()

    def run(self):
        schedule.every(self.config.notifications_frequency).minutes.do(self.check_notification)
        while not self.stop_request.isSet():
            schedule.run_pending()
            time.sleep(1)

    def check_notification(self):
        for client in self.config.notification_clients:
            self.event_queue.put(client.send_notification())

    def join(self, timeout=None):
        self.stop_request.set()
        super(Notifications, self).join(timeout)
