import logging
import psutil

from .models import ApplicationModel
from shared import helper

__APPLICATION_DEFAULT_PATHS = ["Applications"]
__APPLICATION_SUFFIX = ".app"


def get_running_applications(proc_iter, username):
    applications_model = []
    for process in proc_iter:
        try:
            if process.username() == username:
                for process_file in process.open_files():
                    if any(macos_app_path in process_file.path for macos_app_path in __APPLICATION_DEFAULT_PATHS):
                        application_name = process_file.path.split("/")[2]
                        if __APPLICATION_SUFFIX in application_name:
                            application_model = ApplicationModel(
                                path=process_file.path,
                                fullname=application_name,
                                name=helper.remove_suffix(application_name, __APPLICATION_SUFFIX),
                                pid=process.pid
                            )
                            if any(_applications_model.fullname == application_model.fullname for _applications_model in
                                   applications_model):
                                continue
                            applications_model.append(application_model)
                        break
        except psutil.AccessDenied:
            pass
    return applications_model
