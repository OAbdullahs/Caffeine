import ctypes
import time

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate

_keep_cpu_up = None


def set_keep_awake(screen_on=False):
    global _keep_cpu_up
    _keep_cpu_up = True

    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if screen_on:
        flags |= ES_DISPLAY_REQUIRED

    ctypes.windll.kernel32.SetThreadExecutionState(flags)

    SPINNING_CHARS = ["|", "/", "-", "\\"]
    while _keep_cpu_up:
        for i in range(0, 4):
            # Do nothing
            time.sleep(1)


def unset_keep_awake():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    global _keep_cpu_up
    _keep_cpu_up = False
