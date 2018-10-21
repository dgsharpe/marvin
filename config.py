import json

from inotify_simple import flags
from notifications.mailgun import Mailgun
from notifications.pushover import Pushover
from notifications.local_mail import LocalMail


class Config:
    watch_flags = 0
    watch_paths = []
    excluded_paths = []
    notification_clients = []

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        with open(config_file_path, 'r') as f:
            config = json.load(f)

            self.log_file_path = config["logFilePath"]

            for path in config["watchPaths"]:
                self.watch_paths.append(path)

            for path in config["excludedPaths"]:
                self.excluded_paths.append(path)

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

            if "notifications" in config:
                self.notifications_frequency = config["notifications"]["frequencyInMinutes"]
                if "mailgun" in config["notifications"]:
                    if "enabled" not in config["notifications"]["mailgun"] or config["notifications"]["mailgun"]["enabled"]:
                        mailgun_api_key = config["notifications"]["mailgun"]["apiKey"]
                        mailgun_domain_name = config["notifications"]["mailgun"]["domainName"]
                        mailgun_email_address = config["notifications"]["mailgun"]["emailAddress"]
                        mailgun_client = Mailgun(self, mailgun_api_key, mailgun_domain_name, mailgun_email_address)
                        self.notification_clients.append(mailgun_client)
                if "localMail" in config["notifications"]:
                    if "enabled" not in config["notifications"]["localMail"] or config["notifications"]["localMail"]["enabled"]:
                        local_mail_email_address = config["notifications"]["localMail"]["emailAddress"]
                        local_mail_client = LocalMail(self, local_mail_email_address)
                        self.notification_clients.append(local_mail_client)
                if "pushover" in config["notifications"]:
                    if "enabled" not in config["notifications"]["pushover"] or config["notifications"]["pushover"]["enabled"]:
                        pushover_app_token = config["notifications"]["pushover"]["appToken"]
                        pushover_user_key = config["notifications"]["pushover"]["userKey"]
                        pushover_client = Pushover(self, pushover_app_token, pushover_user_key)
                        self.notification_clients.append(pushover_client)
