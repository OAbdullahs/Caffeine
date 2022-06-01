import time


def start_timer(hours, minutes, callback):
    hours_to_seconds = int(hours) * 3600
    minutes_to_seconds = int(minutes) * 60
    remaining_seconds = hours_to_seconds + minutes_to_seconds

    while remaining_seconds != 0:
        remaining_seconds -= 1
        callback(remaining_seconds)
        time.sleep(1)
