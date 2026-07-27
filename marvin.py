import logging
import queue
import sys

from config import Config
from file_event import FileEvent
from file_monitor import FileMonitor
from logger import Logger
from notifications.notification_event import NotificationEvent
from notifications.notifications import Notifications

THREAD_JOIN_TIMEOUT_SECONDS = 10


def shutdown(threads):
    for thread in threads:
        thread.join(THREAD_JOIN_TIMEOUT_SECONDS)
    logging.shutdown()


if __name__ == "__main__":

    config = Config("config.json")
    logger = Logger(config)

    file_event_queue = queue.Queue()
    file_monitor = FileMonitor(config, file_event_queue)
    notifications = Notifications(config, file_event_queue)
    threads = {"file monitor": file_monitor, "notifications": notifications}

    try:
        file_monitor.start()
        notifications.start()
        while True:
            for name, thread in threads.items():
                if not thread.is_alive():
                    logging.critical("The %s thread has died. Exiting so the service manager can restart Marvin", name)
                    shutdown(threads.values())
                    sys.exit(1)
            try:
                event = file_event_queue.get(timeout=5)
                if isinstance(event, FileEvent):
                    logger.log_file_event(event)
                elif isinstance(event, NotificationEvent):
                    logger.log_notification_event(event)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        shutdown(threads.values())
        sys.exit()
