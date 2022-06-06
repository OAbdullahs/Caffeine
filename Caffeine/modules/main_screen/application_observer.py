import os
import threading
import customtkinter
import tkinter

from PIL import ImageTk, Image
from modules.caffeine.caffeine import enable_coffeine, disable_coffeine


class ProcessObserverFrame:

    def __init__(self, app: customtkinter.CTk):
        self.__setup(app)

    def __setup(self, app):
        customtkinter.CTkLabel(text="", master=app, height=1).grid(row=6, column=0)
        application_observer_label = customtkinter.CTkLabel(master=app, text="Select from running application")
        application_observer_label.grid(row=7, column=0, ipadx=12, sticky="w")
        main_frame = customtkinter.CTkFrame(master=app)
        main_frame.grid(row=8, column=0, padx=20, sticky="we")

        img = ImageTk.PhotoImage(Image.open("icons/caffeine.ico"))
        application_icon = customtkinter.CTkLabel(master=main_frame, image=img)
        application_icon.grid(row=0, column=0)
