__version__ = "0.0.1"

import logging
import platform
import time

import psutil
import getpass

import shared.falgs as flags

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


def get_all_running_applications(result, on_watch_application_closed):
    global __applications_model
    global __being_watched
    is_being_watched_closed = True
    try:
        while True and not flags.exit_flag:
            applications_result = get_running_applications(psutil.process_iter(), getpass.getuser())
            if __applications_model != applications_result:
                for application in applications_result:
                    if __being_watched[0] == application.fullname:
                        if __being_watched[0] != "":
                            is_being_watched_closed = False
                        application.set_watching(__being_watched[1])
                result(applications_result)
                __applications_model = applications_result
            time.sleep(5)  # TODO Reduce time
            if is_being_watched_closed and __being_watched[0] != "":
                on_watch_application_closed(__being_watched[0])
                __being_watched = ("", False)
    except:
        logging.error("Getting applications stopped")


def update_list(pid, watch):
    global __applications_model
    global __being_watched

    if pid == 0:
        __being_watched = ("", False)

    for application in __applications_model:
        if application.pid == pid:
            __being_watched = (application.fullname, watch)
            application.set_watching(watch)
