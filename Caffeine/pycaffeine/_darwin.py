from subprocess import Popen, PIPE

# See: https://ss64.com/osx/caffeinate.html
COMMAND = u"caffeinate"

ARGS = [
    "-d",  # Prevent the display from sleeping.
    "-u",  # Create an assertion to declare that user is active. If the dis-
    # play is off, this option turns the display on and prevents the
    # display from going into idle sleep.
    "-t 2592000",  # Set timeout to 1-month (default is 5 seconds for -u option)
]

_process = None


def set_keep_awake(screen_on=False):
    if screen_on:
        global _process
        _process = Popen([COMMAND] + ARGS, stdin=PIPE, stdout=PIPE)
    else:
        _process = Popen([COMMAND], stdin=PIPE, stdout=PIPE)


def unset_keep_awake():
    global _process

    _process.terminate()
    _process.wait()
