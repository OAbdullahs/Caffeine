import os
import threading

import customtkinter
import tkinter
from tkinter.filedialog import askopenfilename

from modules.caffeine.caffeine import _enable_coffeine, _disable_coffeine
from shared.file_watcher import MyWatchDog


class FileObserverFrame:
    __is_caffeine_enabled = False

    def __init__(self, app: customtkinter.CTk):
        customtkinter.CTkLabel(text="", master=app, height=1).grid(row=3, column=0)
        file_observer_label = customtkinter.CTkLabel(text="While file is downloading", master=app)
        file_observer_label.grid(row=4, column=0, ipadx=12, sticky="w")

        main_frame = customtkinter.CTkFrame(master=app)
        main_frame.grid(row=5, column=0, padx=20, sticky="we")

        open_file_label = customtkinter.CTkLabel(text="Select a file: ", master=main_frame)
        open_file_label.grid(row=0, column=0)

        file_picker_button = customtkinter.CTkButton(text="Choose", master=main_frame,
                                                     command=self.__on_file_picker_button_clicked)
        file_picker_button.grid(row=0, column=1, pady=10)

        self.watching_status_frame = customtkinter.CTkFrame(master=app)
        self.watching_status_label = customtkinter.CTkLabel(master=self.watching_status_frame)
        self.watching_status_label.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

    def __on_file_picker_button_clicked(self):
        tkinter.Tk().withdraw()
        filepath = askopenfilename()
        if filepath != "":
            self.watching_status_frame.grid(row=5, column=1, sticky="nsew")
            self.watching_status_label["text"] = f"Watching: \n{os.path.basename(filepath)}"
            my_watcher = MyWatchDog(filepath)
            my_watcher.on_finish_callback = self.__on_file_watch_complete
            threading.Thread(target=my_watcher.run).start()
            threading.Thread(target=_enable_coffeine).start()
        else:
            self.watching_status_frame.grid_forget()

    def __on_file_watch_complete(self, filename):
        threading.Thread(target=_disable_coffeine).start()
        self.watching_status_label["text"] = f"Done Watching: \n{filename}"
