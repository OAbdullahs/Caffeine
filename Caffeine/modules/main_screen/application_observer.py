import logging
import threading
import customtkinter
import tkinter

from PIL import Image, ImageTk

from modules.caffeine.caffeine import enable_coffeine, disable_coffeine
from pyprocess import get_all_running_applications, update_list


class ProcessObserverFrame:
    __is_caffeine_on = False

    def __init__(self, app: customtkinter.CTk, application_path):
        self.application_path = application_path
        threading.Thread(target=get_all_running_applications,
                         args=(self.__init_applications,)).start()
        self.__setup(app)

    def __setup(self, app):
        customtkinter.CTkLabel(text="", master=app, height=1).grid(row=6, column=0)
        application_observer_label = customtkinter.CTkLabel(master=app, text="Select from running application")
        application_observer_label.grid(row=7, column=0, ipadx=12, sticky="w")
        self.main_frame = customtkinter.CTkFrame(master=app)
        self.main_frame.grid(row=8, column=0, padx=20, sticky="we")

    def __init_applications(self, applications):
        self.__clear_frame_widget()
        for application in applications:
            application_frame = self.application_frame(application)
            application_frame.pack(fill=tkinter.X, pady=5, padx=5)

    def __clear_frame_widget(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def application_frame(self, application):
        application_frame = customtkinter.CTkFrame(master=self.main_frame)
        image = Image.open(application.icon_path()).resize((48, 48))
        tkinter_image = ImageTk.PhotoImage(image)
        application_icon = customtkinter.CTkLabel(master=application_frame, height=48, width=48)
        application_icon.image = tkinter_image
        application_icon.config(image=tkinter_image)
        application_icon.pack(side=tkinter.LEFT)
        application_name_label = customtkinter.CTkLabel(master=application_frame, text=application.name)
        application_name_label.pack(side=tkinter.LEFT)
        application_watch_button = customtkinter.CTkButton(master=application_frame,
                                                           text="Watch" if not application.is_being_watched() else "Stop watching")
        application_watch_button.config(
            command=lambda name=application.name, pid=application.pid,
                           button=application_watch_button: self.on_watch_clicked(name, pid, button))
        application_watch_button.pack(side=tkinter.RIGHT, padx=5)
        return application_frame

    def on_watch_clicked(self, name, pid, button):
        if not self.__is_caffeine_on:
            logging.info("Watching: " + name)
            button.set_text("Stop Watching")
            threading.Thread(target=enable_coffeine).start()
            update_list(pid, True)
            self.__is_caffeine_on = True
        else:
            logging.info("Stopped watching: " + name)
            self.__is_caffeine_on = False
            threading.Thread(target=disable_coffeine).start()
            update_list(pid, False)
            button.set_text("Watch")
