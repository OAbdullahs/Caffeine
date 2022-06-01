import tkinter

import customtkinter
import threading
import datetime
from modules.caffeine.caffeine import (_enable_coffeine, _disable_coffeine)
from shared.timer import start_timer


def _is_entry_only_digit(value):
    if str.isdigit(value):
        if int(value) > 0:
            return True
        else:
            return False
    else:
        return False


class TimeFrame:
    __is_indefinitely_enabled = False

    def __init__(self, app: customtkinter.CTk):
        app.title("Coffiene")
        self.__time_interval_frame(app)

    def __time_interval_frame(self, app):
        main_frame = customtkinter.CTkFrame(master=app)
        main_frame.pack(pady=20, padx=60, fill="both", expand=False, anchor="w")

        timer_label = customtkinter.CTkLabel(text="Select a time", master=main_frame)
        timer_label.grid(row=1, column=1)

        indefinitely_label = customtkinter.CTkLabel(text="Indefinitely:", master=main_frame)
        indefinitely_label.grid(row=2, column=1)

        self.indefinitely_button = customtkinter.CTkButton(text="Enable", master=main_frame,
                                                           command=self.__on_indefinitely_button_clicked)
        self.indefinitely_button.grid(row=2, column=2)

        until_label = customtkinter.CTkLabel(text="Time/Until:", master=main_frame)
        until_label.grid(row=3, column=1)

        vcmd = main_frame.register(_is_entry_only_digit)
        on_invalid_hours_cmd = main_frame.register(self.__in_on_invalid_hours_value)
        on_invalid_minutes_cmd = main_frame.register(self.__in_on_invalid_minutes_value)
        self.hours_entry = customtkinter.CTkEntry(placeholder_text="Hours", master=main_frame, validate='focusout',
                                                  validatecommand=(vcmd, "%P"), invalidcommand=on_invalid_hours_cmd)
        self.hours_entry.grid(row=3, column=2, pady=10)

        self.minutes_entry = customtkinter.CTkEntry(placeholder_text="Minutes", master=main_frame, validate='focusout',
                                                    validatecommand=(vcmd, "%P"), invalidcommand=on_invalid_minutes_cmd)
        self.minutes_entry.grid(row=3, column=3, padx=10)

        time_button = customtkinter.CTkButton(master=main_frame, text="Start session",
                                              command=self.__on_start_session_clicked)
        time_button.grid(row=3, column=4, padx=10)

        self.remaining_time_message = customtkinter.CTkLabel(master=main_frame, text="")
        self.remaining_time_message.grid(row=2, column=30)

    def __on_indefinitely_button_clicked(self):
        self.indefinitely_button.set_text("Enable" if self.__is_indefinitely_enabled else "Disable")
        self.__toggle_wakeup_device()

    def __toggle_wakeup_device(self):
        if not self.__is_indefinitely_enabled:
            threading.Thread(target=_enable_coffeine).start()
        else:
            threading.Thread(target=_disable_coffeine).start()

        self.__is_indefinitely_enabled = not self.__is_indefinitely_enabled

    def __in_on_invalid_hours_value(self):
        self.hours_entry.delete(0, tkinter.END)

    def __in_on_invalid_minutes_value(self):
        self.minutes_entry.delete(0, tkinter.END)

    def __on_start_session_clicked(self):
        hours_value = 0 if self.hours_entry.entry.get() == "Hours" else self.hours_entry.entry.get()
        minutes_value = self.minutes_entry.entry.get()
        self.__toggle_wakeup_device()
        self.indefinitely_button.state = tkinter.DISABLED
        threading.Thread(target=start_timer, args=(hours_value, minutes_value, self.update_remaining_time)).start()

    def update_remaining_time(self, remaining_seconds):
        hours, minutes, seconds = str(datetime.timedelta(seconds=remaining_seconds)).split(':')

        hours_text = "" if hours == "0" else f"{hours}:h"
        minutes_text = "" if minutes == "00" else f"{minutes}:m"
        seconds_text = "" if seconds == "0" else f"{seconds}:s"

        text = f"Current session ends in: \n {hours_text} {minutes_text} {seconds_text}"
        self.remaining_time_message["text"] = text

        if remaining_seconds == 0:
            self.remaining_time_message["text"] = ""
            self.indefinitely_button.state = tkinter.NORMAL
            self.__toggle_wakeup_device()
