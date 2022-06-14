__version__ = "0.0.1"

import logging
import platform
import time

import psutil
import getpass

from .models import ApplicationModel

SYSTEM = platform.system().lower()

if SYSTEM == "windows":
    from ._win import get_running_applications
elif SYSTEM == "linux":
    from ._linux import get_running_applications
elif SYSTEM == "darwin":
    from ._darwin import get_running_applications
else:
    NotImplementedError(
        f"pyprocess has not yet a {SYSTEM} implementation. Pull requests welcome: https://github.com/np-8/wakepy"
    )

__applications_model: list[ApplicationModel] = list()


def get_all_running_applications(result):
    global __applications_model
    try:
        while True:
            application_result = get_running_applications(psutil.process_iter(), getpass.getuser())
            if __applications_model != application_result:
                result(application_result)
                __applications_model = application_result
            time.sleep(5)
    except:
        logging.error("Getting applications stopped")


def watch_application(name):
    global __applications_model
    for application_model in __applications_model:
        if name == application_model.name:
            # TODO ADD IMPL
            pass


def get_applications_model():
    global __applications_model
    return __applications_model
