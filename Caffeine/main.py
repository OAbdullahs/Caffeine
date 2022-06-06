import customtkinter
from PIL import Image, ImageTk
from modules.main_screen import (time_frame, file_observer, application_observer)
import logging

logging.basicConfig(
                    format='%(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)
customtkinter.set_appearance_mode("System")

app = customtkinter.CTk()

window_height = 500
window_width = 900

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
app.wm_iconphoto(False, ImageTk.PhotoImage(Image.open("icons/caffeine.ico")))

if __name__ == '__main__':
    time_frame.TimeFrame(app)
    file_observer.FileObserverFrame(app)
    # application_observer.ProcessObserverFrame(app)
    app.mainloop()
