import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

__file_size = None


class MyWatchDog:
    __keep_watching = True

    on_finish_callback = None

    def __init__(self, filepath):
        self.event_handler = Handler()
        self.event_handler.on_finish_callback = self.on_finish
        self.observer = Observer()
        self.filepath = filepath

    def run(self):
        print("Watching " + self.filepath + "\n")
        self.event_handler.filepath = self.filepath
        self.observer.schedule(self.event_handler, os.path.dirname(self.filepath), recursive=True)
        self.observer.start()
        try:
            while self.__keep_watching:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

    def on_finish(self):
        print("Stopped watching " + self.filepath)
        self.__keep_watching = False
        self.observer.stop()
        self.on_finish_callback(os.path.basename(self.filepath))


class Handler(FileSystemEventHandler):
    filepath = None
    on_finish_callback = None

    def on_any_event(self, event):
        if event.src_path == self.filepath:
            print(str(event))
            self.on_finish_callback()
