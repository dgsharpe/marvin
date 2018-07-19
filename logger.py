import logging
import logging.handlers

from inotify_simple import flags
from notificationevent import NotificationEventType


class Logger:

    def __init__(self, config):
        self.watchFlags = config.watch_flags

        LOGGING_MSG_FORMAT = '[%(levelname)s] [%(asctime)s] : %(message)s'
        LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

        logging.basicConfig(
            level=logging.DEBUG,
            format=LOGGING_MSG_FORMAT,
            datefmt=LOGGING_DATE_FORMAT
        )

        formatter = logging.Formatter(LOGGING_MSG_FORMAT)
        handler = logging.handlers.TimedRotatingFileHandler(filename=config.log_file_path, when="d", interval=1,
                                                            backupCount=7)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        logging.getLogger('schedule').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    def log_file_event(self, file_event):
        actionable_flags = flags.from_mask((self.watchFlags ^ flags.ISDIR ^ flags.Q_OVERFLOW) & file_event.mask)
        if len(actionable_flags) > 0:
            log_string = ""
            for flag in actionable_flags:
                log_string += str(flag)[6:] + ", "
            log_string = log_string[:-2]
            log_string += " " + file_event.full_path
            if flags.Q_OVERFLOW & file_event.mask:
                self.logger.error(log_string)
                self.logger.error("INOTIFY QUEUE OVERFLOW DETECTED - some events may not have been logged!")
            else:
                self.logger.info(log_string)

    def log_notification_event(self, event):
        if event.eventType == NotificationEventType.EMAIL_SENT:
            self.logger.info("Notification email sent")
        elif event.eventType == NotificationEventType.EMAIL_FAILURE:
            self.logger.error("Notification email failed to send")
        elif event.eventType == NotificationEventType.PUSHOVER_SENT:
            self.logger.info("Pushover notification sent")
        elif event.eventType == NotificationEventType.PUSHOVER_FAILURE:
            self.logger.error("Pushover notification failed to send")
