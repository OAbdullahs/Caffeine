import customtkinter

customtkinter.set_appearance_mode("System")

app = customtkinter.CTk()

window_height = 500
window_width = 900

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

if __name__ == '__main__':
    app.mainloop()
