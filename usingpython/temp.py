import customtkinter
import tkinter
import threading

Constdata = {"BACKGROUND_COLOR": "#333333"}

class App(customtkinter.CTk):
    frames = {}
    username = None

    def __init__(self):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        super().__init__()
        self.title("Chatting Application")
        self.geometry("1000x650+50+50")

        main_container = customtkinter.CTkFrame(self)
        main_container.grid(row=0, column=0)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        App.frames['page1'] = customtkinter.CTkFrame(main_container, fg_color=Constdata["BACKGROUND_COLOR"])
        App.frames['page1'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        App.frames['page2'] = customtkinter.CTkFrame(main_container, fg_color=Constdata["BACKGROUND_COLOR"])
        App.frames['page2'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        self.login_entry = customtkinter.CTkEntry(App.frames['page1'])
        self.login_entry.pack(pady=20)
        self.login_button = customtkinter.CTkButton(App.frames['page1'], text="Login", command=self.handle_login)
        self.login_button.pack(pady=20)

        self.page1_selector()

    def page1_selector(self):
        for frame in App.frames.values():
            frame.pack_forget()
        App.frames['page1'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def chat_page(self):
        for frame in App.frames.values():
            frame.pack_forget()
        App.frames['page2'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def handle_login(self):
        App.username = self.login_entry.get()
        if App.username:  # Check if username is not empty
            print(f"Username entered: {App.username}")
            self.chat_page()

    def get_username(self):
        return App.username

# Function to run the frontend in a separate thread
def frontend_thread():
    global frontend_obj
    frontend_obj = App()
    frontend_obj.mainloop()

# Start the frontend thread
thread = threading.Thread(target=frontend_thread, args=()).start()

# frontend_obj = App()

# Simulate the main program waiting for the username to be entered
while frontend_obj.get_username() is None:
    pass

print(f"Username from main program: {frontend_obj.get_username()}")
