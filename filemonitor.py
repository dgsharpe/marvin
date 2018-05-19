import os
import threading

from inotify_simple import INotify, flags
from fileevent import FileEvent


class FileMonitor(threading.Thread):

    def __init__(self, config, event_queue):
        super(FileMonitor, self).__init__()
        self.stop_request = threading.Event()
        self.inotify = INotify()
        self.event_queue = event_queue
        self.watch_paths = config.watch_paths
        self.watch_flags = config.watch_flags
        self.recursion = config.recursion
        self.watch_descriptor_paths = {}

    def run(self):
        for path in self.watch_paths:
            self.__add_watch(path)
            if self.recursion:
                for root, dirs, files in os.walk(path):
                    if root not in self.watch_descriptor_paths:
                        self.__add_watch(root)
        while not self.stop_request.isSet():
            for event in self.inotify.read(timeout=5):
                file_event = FileEvent(event, self.watch_descriptor_paths[event[0]])
                if self.recursion and flags.ISDIR & file_event.mask and flags.CREATE & file_event.mask:
                    self.__add_watch(file_event.full_path)
                if flags.DELETE_SELF & file_event.mask:
                    self.__rm_watch(file_event.full_path)
                self.event_queue.put(file_event)

    def __add_watch(self, path):
        wd = self.inotify.add_watch(path, self.watch_flags)
        self.watch_descriptor_paths[wd] = path
        self.watch_descriptor_paths[path] = wd
        for root, dirs, files in os.walk(path):
            if root not in self.watch_descriptor_paths:
                self.__add_watch(root)

    def __rm_watch(self, path):
        try:
            wd = self.watch_descriptor_paths[path]
            del self.watch_descriptor_paths[path]
            del self.watch_descriptor_paths[wd]
        except KeyError:
            if not path.endswith('/'):
                path = path + "/"
                wd = self.watch_descriptor_paths[path]
                del self.watch_descriptor_paths[path]
                del self.watch_descriptor_paths[wd]

    def join(self, timeout=None):
        self.stop_request.set()
        super(FileMonitor, self).join(timeout)
