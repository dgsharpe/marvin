class NotificationClient:
    NOTIFICATION_LOG_MESSAGE = ""
    NOTIFICATION_FAILED_LOG_MESSAGE = ""

    def __init__(self, config):
        self.config = config

    def log_lines_since(self, log_message):
        log_lines = ""
        for line in reversed(open(self.config.log_file_path).readlines()):
            if log_message not in line:
                log_lines = line + log_lines
            else:
                break

        return log_lines

    def send_notification(self):
        raise Exception("Send notification should not be called on NotificationClient")
