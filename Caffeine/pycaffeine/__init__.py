__version__ = "0.5.0"

import platform

SYSTEM = platform.system().lower()

if SYSTEM == "windows":
    from ._win import set_keep_awake, unset_keep_awake
elif SYSTEM == "linux":
    from ._linux import set_keep_awake, unset_keep_awake
elif SYSTEM == "darwin":
    from ._darwin import set_keep_awake, unset_keep_awake
else:
    NotImplementedError(
        f"pycaffeine has not yet a {SYSTEM} implementation. Pull requests welcome: https://github.com/np-8/wakepy"
    )


def keep_awake(keep_screen_on=False):
    set_keep_awake(keep_screen_on)


def stop_keep_awake():
    unset_keep_awake()
