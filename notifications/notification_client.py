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
                # If the client type is not in the line, don't include this
                # line, but dont stop adding lines. This means sending an email
                # won't include the log for sending a push notificaiton, but
                # previous logs will be included
                pass
            else:
                break

        return log_lines

    def send_notification(self):
        raise Exception("Send notification should not be called on NotificationClient")
