import os


class NotificationClient:
    NOTIFICATION_LOG_MESSAGE = "Notification sent: "
    NOTIFICATION_FAILED_LOG_MESSAGE = "Notification failed: "

    def __init__(self, config):
        self.config = config

    def log_lines_since_last_notification(self, client_type):
        # Get a list of the log files which exist, sorted from most recent to least recent.
        log_file_directory = self.config.log_file_path.rsplit("/", 1)[0]
        log_file_name = self.config.log_file_path.rsplit("/", 1)[1]
        log_files = [self.config.log_file_path] + sorted(
            [file for file in os.listdir(log_file_directory) if log_file_name in file and log_file_name != file], reverse=True
        )

        log_lines = ""
        last_notification_send_found = False

        # Iterate through the lines in the log files, stopping when we see the most recent notification send
        for log_file in log_files:
            for line in reversed(open(log_file).readlines()):
                if self.NOTIFICATION_LOG_MESSAGE not in line:
                    # If the line isn't for sending a notification
                    log_lines = line + log_lines
                elif client_type not in line:
                    # If this log line is about a notification, but pertains
                    # to a different notification client than the current one,
                    # omit the line and continue.
                    pass
                else:
                    last_notification_send_found = True
                    break
            if last_notification_send_found:
                break

        return log_lines

    def send_notification(self):
        raise Exception(
            "send_notification method should not be called on NotificationClient, only on its inheriting classes"
        )
