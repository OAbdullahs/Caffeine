import logging
import pycaffeine


def enable_coffeine():
    logging.info("Starting caffeinate on Mac OS")
    pycaffeine.keep_awake(True)


def disable_coffeine():
    logging.info("Disabling caffeinate on Mac OS ")
    pycaffeine.stop_keep_awake()
