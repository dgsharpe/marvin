import os
import threading

from inotify_simple import INotify, flags
from file_event import FileEvent

READ_TIMEOUT_MS = 1000


class FileMonitor(threading.Thread):
    def __init__(self, config, event_queue):
        super(FileMonitor, self).__init__()
        self.stop_request = threading.Event()
        self.inotify = INotify()
        self.event_queue = event_queue
        self.watch_paths = config.watch_paths
        self.excluded_paths = [os.path.abspath(path) for path in config.excluded_paths]
        self.watch_flags = config.watch_flags
        self.recursion = config.recursion
        self.log_file_path = os.path.abspath(config.log_file_path)
        self.watch_descriptor_paths = {}
        self.draining = False

    def run(self):
        for path in self.watch_paths:
            self.__add_watches(path)
        while not self.stop_request.is_set():
            self.__handle_events(self.inotify.read(timeout=READ_TIMEOUT_MS))

    def __handle_events(self, events):
        for event in events:
            parent_path = self.watch_descriptor_paths.get(event[0])
            if parent_path is None:
                # A queue overflow is reported against watch descriptor -1
                if flags.Q_OVERFLOW & event[1]:
                    self.event_queue.put(FileEvent(event, ""))
                continue
            file_event = FileEvent(event, parent_path)
            if self.recursion and flags.ISDIR & file_event.mask and flags.CREATE & file_event.mask:
                self.__add_watches(file_event.full_path)
            if flags.DELETE_SELF & file_event.mask:
                self.__rm_watch(file_event.full_path)
            if self.__is_own_log_file(file_event.full_path):
                continue
            self.event_queue.put(file_event)

    def __drain_pending_events(self):
        # Keeps events flowing while a large tree is still being walked
        if self.draining:
            return
        self.draining = True
        try:
            self.__handle_events(self.inotify.read(timeout=0))
        finally:
            self.draining = False

    def __is_own_log_file(self, path):
        path = os.path.abspath(path)
        # Trailing "." matches TimedRotatingFileHandler's rotated names, not siblings
        return path == self.log_file_path or path.startswith(self.log_file_path + ".")

    def __is_excluded(self, path):
        path = os.path.abspath(path)
        for excluded_path in self.excluded_paths:
            if path == excluded_path or path.startswith(excluded_path + os.sep):
                return True
        return False

    def __add_watches(self, path):
        if self.__is_excluded(path):
            return
        self.__add_watch(path)
        if not self.recursion:
            return
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not self.__is_excluded(os.path.join(root, d))]
            for directory in dirs:
                self.__add_watch(os.path.join(root, directory))
            self.__drain_pending_events()

    def __add_watch(self, path):
        wd = self.inotify.add_watch(path, self.watch_flags)
        self.watch_descriptor_paths[wd] = path
        self.watch_descriptor_paths[path] = wd

    def __rm_watch(self, path):
        try:
            wd = self.watch_descriptor_paths[path]
            del self.watch_descriptor_paths[path]
            del self.watch_descriptor_paths[wd]
        except KeyError:
            if not path.endswith("/"):
                path = path + "/"
                wd = self.watch_descriptor_paths[path]
                del self.watch_descriptor_paths[path]
                del self.watch_descriptor_paths[wd]

    def join(self, timeout=None):
        self.stop_request.set()
        super(FileMonitor, self).join(timeout)
