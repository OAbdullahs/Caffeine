import logging
import os
from pathlib import Path
import time
from .helper import remove_suffix
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOWNLOADING_TYPES = [".part"]


class MyWatchDog:
    __keep_watching = True
    __filename = ""
    on_finish_callback = None

    def __init__(self, filepath):
        self.event_handler = Handler()
        self.event_handler.on_finish_callback = self.on_finish
        self.observer = Observer()
        self.filepath = filepath
        self.__set_file_name()
        self.event_handler.set_filename(self.__filename)

    def __set_file_name(self):
        filepath = Path(self.filepath)
        filename = filepath.name
        filetype = filepath.suffix

        if filetype in DOWNLOADING_TYPES:
            logging.info(f"File path:{self.filepath}, name:{filename}, type:{filetype}")
            self.__filename = remove_suffix(filename, filetype)
            return

        self.__filename = filename

    def get_file_name(self):
        return self.__filename

    def run(self):
        logging.info("Watching: " + self.__filename)
        self.event_handler.filepath = self.filepath
        self.observer.schedule(self.event_handler, os.path.dirname(self.filepath), recursive=True)
        self.observer.start()
        try:
            while self.__keep_watching:
                time.sleep(1)
        except:
            self.observer.stop()
            logging.error("Observer Stopped")

        self.observer.join()

    def on_finish(self):
        logging.info("Stopped watching: " + self.__filename)
        self.__keep_watching = False
        self.observer.stop()
        self.on_finish_callback(os.path.basename(self.filepath))

    def force_stop_watching(self):
        logging.info("Force stop watching " + self.__filename)
        self.__keep_watching = False
        self.observer.stop()


class Handler(FileSystemEventHandler):
    __filename = None
    on_finish_callback = None

    def set_filename(self, name):
        self.__filename = name

    def on_moved(self, event):
        logging.info("on_created")
        src_file_suffix = Path(event.src_path).suffix
        modified_filename = remove_suffix(event.src_path, src_file_suffix)
        if self.__is_the_watching_file(modified_filename):
            logging.info(f"file: {event.src_path} || on_moved")
            self.on_finish_callback()

    def on_created(self, event):
        logging.info("on_created")
        if self.__is_the_watching_file(event.src_path):
            logging.info(f"file: {event.src_path} || on_created")
            self.on_finish_callback()

    def on_modified(self, event):
        logging.info("on_modified")
        if self.__is_the_watching_file(event.src_path):
            logging.info(f"file is on_modified")
            self.on_finish_callback()

    def __is_the_watching_file(self, filepath):
        filename = Path(filepath).name
        return filename == self.__filename
