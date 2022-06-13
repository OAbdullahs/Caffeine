import subprocess

COMMAND = u"systemctl"
ARGS = [u"sleep.target", u"suspend.target", u"hibernate.target", u"hybrid-sleep.target"]
# https://www.man7.org/linux/man-pages/man1/systemctl.1.html


try:
    subprocess.check_output(["pidof", "systemd"])
except subprocess.CalledProcessError:
    # if 'pidof' does not find a process it will return with non-zero exit status, check_output will raise
    # subprocess.CalledProcessError See: https://github.com/np-8/wakepy/pull/3
    raise NotImplementedError(
        "pycaffeine has not yet support for init processes other than systemd."
    )


def set_keep_awake(screen_on=False):
    subprocess.run([COMMAND, u"mask", *ARGS])


def unset_keep_awake():
    subprocess.run([COMMAND, u"unmask", *ARGS])
