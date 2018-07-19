import schedule
import threading
import time
import notifications.notificationevent


class Notifications(threading.Thread):
    def __init__(self, config, event_queue):
        super(Notifications, self).__init__()
        self.config = config
        self.eventQueue = event_queue
        self.stop_request = threading.Event()

    def run(self):
        schedule.every(self.config.notifications_frequency).minutes.do(self.check_notification)
        while not self.stop_request.isSet():
            schedule.run_pending()
            time.sleep(1)

    def check_notification(self):
        for client in self.config.notification_clients:
            self.eventQueue.put(client.send_notification())

    def join(self, timeout=None):
        self.stop_request.set()
        super(Notifications, self).join(timeout)
