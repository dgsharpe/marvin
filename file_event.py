from inotify_simple import flags


class FileEvent:
    def __init__(self, event, path):
        self.event = event
        self.wd = event[0]
        self.mask = event[1]
        self.cookie = event[2]
        self.name = event[3]
        self.flags = flags.from_mask(self.mask)
        self.parent_path = path
        self.full_path = path + "/" + self.name
