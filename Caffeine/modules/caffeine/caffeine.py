import logging
import pycaffeine


def enable_coffeine():
    logging.info("Starting caffeine")
    pycaffeine.keep_awake(keep_screen_on=True)


def disable_coffeine():
    logging.info("Disabling caffeine")
    pycaffeine.stop_keep_awake()
