import json

from inotify_simple import flags


class Config:
    watch_flags = 0
    watch_paths = []

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        with open(config_file_path, 'r') as f:
            config = json.load(f)

            self.log_file_path = config["logFilePath"]

            for path in config["watchPaths"]:
                self.watch_paths.append(path)

            for flag, value in config["watchEvents"].items():
                if flag == "access" and value:
                    self.watch_flags = self.watch_flags | flags.ACCESS
                if flag == "attrib" and value:
                    self.watch_flags = self.watch_flags | flags.ATTRIB
                if flag == "close" and value:
                    self.watch_flags = self.watch_flags | flags.CLOSE_WRITE | flags.CLOSE_NOWRITE
                if flag == "create" and value:
                    self.watch_flags = self.watch_flags | flags.CREATE
                if flag == "delete" and value:
                    self.watch_flags = self.watch_flags | flags.DELETE | flags.DELETE_SELF
                if flag == "modify" and value:
                    self.watch_flags = self.watch_flags | flags.MODIFY
                if flag == "move" and value:
                    self.watch_flags = self.watch_flags | flags.MOVED_FROM | flags.MOVED_TO | flags.MOVE_SELF
                if flag == "open" and value:
                    self.watch_flags = self.watch_flags | flags.OPEN
                if flag == "unmount" and value:
                    self.watch_flags = self.watch_flags | flags.UNMOUNT

            self.recursion = config["recursion"]

            if "mailgun" in config:
                self.mailgun_api_key = config["mailgun"]["apiKey"]
                self.mailgun_domain_name = config["mailgun"]["domainName"]
                self.email_address = config["mailgun"]["emailAddress"]
                self.mailgun_frequency = config["mailgun"]["frequencyInMinutes"]
                self.mailgun_enabled = true
            else:
                self.mailgun_enabled = false
