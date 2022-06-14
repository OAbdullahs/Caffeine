import os
from dataclasses import dataclass
import psutil


@dataclass
class ApplicationModel:
    path: str
    fullname: str
    name: str
    pid: int
    __is_being_watched = False
    __IMAGES_EXT = [".ico", ".icns"]
    __COMMON_ICON_NAME = "AppIcon"

    def __init__(self, path, fullname, name, pid):
        self.path = path
        self.fullname = fullname
        self.name = name
        self.pid = pid

    def is_running(self):
        process = psutil.Process(pid=self.pid)
        if process.name() == self.name:
            return process.is_running()
        else:
            return False

    def icon_path(self):
        res_path = "/Applications" + f"/{self.fullname}/Contents/Resources"
        if any(self.__COMMON_ICON_NAME in name for name in os.listdir(res_path)):
            return res_path + f"/AppIcon.icns"
        for res_dir in os.listdir(res_path):
            if any(image_ext in res_dir for image_ext in self.__IMAGES_EXT):
                return res_path + f"/{res_dir}"

        # TODO ADD MISSING IMAGE
        return None

    def is_being_watched(self):
        return self.__is_being_watched

    def set_watching(self, watching):
        self.__is_being_watched = watching
