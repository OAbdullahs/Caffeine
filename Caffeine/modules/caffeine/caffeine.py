import wakepy


def _enable_coffeine():
    print("Starting caffeinate on Mac OS")
    wakepy.set_keepawake(True)


def _disable_coffeine():
    print("Disabling caffeinate on Mac OS ")
    wakepy.unset_keepawake()



