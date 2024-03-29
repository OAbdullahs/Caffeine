import os

import customtkinter
from PIL import ImageTk
from PIL import Image

from modules.main_screen import (time_frame, file_observer, application_observer)
from modules.caffeine.caffeine import disable_coffeine
from tkinter import messagebox
import shared.falgs as flags
import logging

__version__ = "0.0.1"
__status__ = "dev"

logging.basicConfig(
    # filename="Caffeine.log",
    format='%(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.DEBUG)

logging.critical(f"caffeine version:{__version__}, status:{__status__}")
customtkinter.set_appearance_mode("System")

app = customtkinter.CTk()
application_path = os.path.dirname(os.path.realpath(__file__))

window_height = 500
window_width = 900

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
app.wm_iconphoto(False, ImageTk.PhotoImage(Image.open(application_path + "/Resources/caffeine.ico")))


def local_disable_caffeine():
    disable_coffeine()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        flags.exit_flag = True
        # local_disable_caffeine()
        app.destroy()


if __name__ == '__main__':
    time_frame.TimeFrame(app)
    file_observer.FileObserverFrame(app)
    application_observer.ProcessObserverFrame(app, application_path)
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

# atexit.register(local_disable_caffeine)
# signal.signal(signal.SIGTERM, local_disable_caffeine)
# signal.signal(signal.SIGINT, local_disable_caffeine)
