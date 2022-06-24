import time
import shared.falgs as flags
__is_timer_canceled = False


def start_timer(hours, minutes, callback):
    global __is_timer_canceled
    __is_timer_canceled = False
    hours_to_seconds = int(hours) * 3600
    minutes_to_seconds = int(minutes) * 60
    remaining_seconds = hours_to_seconds + minutes_to_seconds

    while remaining_seconds != 0:
        remaining_seconds -= 1
        callback(remaining_seconds)
        time.sleep(1)

        if __is_timer_canceled or flags.exit_flag:
            callback(0)
            break


def cancel_timer():
    global __is_timer_canceled
    __is_timer_canceled = True
