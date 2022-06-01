import customtkinter
import tkinter
from tkinter.filedialog import askopenfilename


class FileObserverFrame:

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

    @staticmethod
    def __on_file_picker_button_clicked():
        tkinter.Tk().withdraw()
        file_name = askopenfilename()
        print("file name = " + file_name)
