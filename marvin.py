import logging
import queue

from config import Config
from fileevent import FileEvent
from filemonitor import FileMonitor
from logger import Logger
from notifications.notificationevent import NotificationEvent
from notifications.notifications import Notifications

if __name__ == "__main__":

    config = Config('config.json')
    logger = Logger(config)

    file_event_queue = queue.Queue()
    file_monitor = FileMonitor(config, file_event_queue)
    notifications = Notifications(config, file_event_queue)

    try:
        file_monitor.start()
        notifications.start()
        while True:
            try:
                event = file_event_queue.get(timeout=5)
                if isinstance(event, FileEvent):
                    logger.log_file_event(event)
                elif isinstance(event, NotificationEvent):
                    logger.log_notification_event(event)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        file_monitor.join()
        notifications.join()
        logging.shutdown()
        exit()
