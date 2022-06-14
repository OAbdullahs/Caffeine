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
__being_watched = ("", False)


def get_all_running_applications(result):
    global __applications_model
    try:
        while True:
            applications_result = get_running_applications(psutil.process_iter(), getpass.getuser())
            if __applications_model != applications_result:
                for application in applications_result:
                    if __being_watched[0] == application.fullname:
                        application.set_watching(__being_watched[1])
                result(applications_result)
                __applications_model = applications_result
            time.sleep(5)
    except:
        logging.error("Getting applications stopped")


def watch_application(name):
    global __applications_model
    for application_model in __applications_model:
        if name == application_model.name:
            # TODO ADD IMPL
            pass


def update_list(pid, watch):
    global __applications_model
    global __being_watched

    if pid == 0:
        __being_watched = ("", False)

    for application in __applications_model:
        if application.pid == pid:
            __being_watched = (application.fullname, watch)
            application.set_watching(watch)
