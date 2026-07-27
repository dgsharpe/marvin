import os

TRUNCATION_NOTICE = "... truncated: earlier lines omitted because the notification size cap was reached\n"


def read_lines_reverse(file_path, chunk_size=8192):
    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        remaining = f.tell()
        read_any = False
        trailer = b""
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            remaining -= read_size
            f.seek(remaining)
            lines = (f.read(read_size) + trailer).split(b"\n")
            trailer = lines.pop(0)
            if not read_any:
                read_any = True
                # A file ending in a newline splits to a final empty element
                if lines and lines[-1] == b"":
                    lines.pop()
            for line in reversed(lines):
                yield line.decode("utf-8", "replace") + "\n"
        if read_any:
            yield trailer.decode("utf-8", "replace") + "\n"


class NotificationClient:
    NOTIFICATION_LOG_MESSAGE = "Notification sent: "
    NOTIFICATION_FAILED_LOG_MESSAGE = "Notification failed: "

    def __init__(self, config):
        self.config = config

    def log_lines_since_last_notification(self, client_type):
        # Get a list of the log files which exist, sorted from most recent to least recent.
        log_file_directory = os.path.dirname(self.config.log_file_path) or "."
        log_file_name = os.path.basename(self.config.log_file_path)
        log_files = [self.config.log_file_path] + sorted(
            [
                os.path.join(log_file_directory, file)
                for file in os.listdir(log_file_directory)
                if log_file_name in file and log_file_name != file
            ],
            reverse=True,
        )
        log_lines = []
        log_bytes = 0
        truncated = False
        finished = False

        # Iterate backwards through the lines in the log files, stopping when we see the most
        # recent notification send or when the configured size caps are reached.
        for log_file in log_files:
            if finished:
                break
            for line in read_lines_reverse(log_file):
                if self.NOTIFICATION_LOG_MESSAGE in line:
                    if client_type in line:
                        finished = True
                        break
                    # This line is about a notification, but pertains to a different
                    # notification client than the current one, so omit it and continue.
                    continue
                if (
                    len(log_lines) >= self.config.notifications_max_lines
                    or log_bytes + len(line) > self.config.notifications_max_bytes
                ):
                    truncated = True
                    finished = True
                    break
                log_lines.append(line)
                log_bytes += len(line)

        if truncated:
            log_lines.append(TRUNCATION_NOTICE)

        return "".join(reversed(log_lines))

    def send_notification(self):
        raise Exception(
            "send_notification method should not be called on NotificationClient, only on its inheriting classes"
        )
