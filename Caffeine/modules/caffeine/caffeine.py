import wakepy
import logging


def enable_coffeine():
    logging.info("Starting caffeinate on Mac OS")
    wakepy.set_keepawake(True)


def disable_coffeine():
    logging.info("Disabling caffeinate on Mac OS ")
    wakepy.unset_keepawake()



