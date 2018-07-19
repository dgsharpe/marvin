class NotificationClient:
    NOTIFICATION_LOG_MESSAGE = "Notification sent: "
    NOTIFICATION_FAILED_LOG_MESSAGE = "Notification failed: "

    def __init__(self, config):
        self.config = config

    def log_lines_since_last_notification(self, client_type):
        log_lines = ""
        for line in reversed(open(self.config.log_file_path).readlines()):
            if self.NOTIFICATION_LOG_MESSAGE not in line:
                # If the line isn't for sending a notification
                log_lines = line + log_lines
            elif client_type not in line:
                # If this log line is about a notification, but pertains
                # to a different notification client than the current one,
                # omit the line and continue.
                pass
            else:
                break

        return log_lines

    def send_notification(self):
        raise Exception("send_notification method should not be called on NotificationClient, only on its inheriting classes")
