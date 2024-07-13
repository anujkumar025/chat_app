import tkinter
import customtkinter
from PIL import Image
from data import Constdata
import time


class App(customtkinter.CTk):

    frames = {"page1": None, "page2": None}
    username = None
    new_message = None
    member_container = None
    message_container = None

    def page1_selector(self):
        App.frames["page2"].pack_forget()
        App.frames["page1"].pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.login_page()

    def page2_selector(self):
        App.frames["page1"].pack_forget()
        App.frames["page2"].pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.chatting_page()
    
    def login_page(self):
        enter_name_label = customtkinter.CTkLabel(App.frames['page1'], text="Enter Username", anchor=tkinter.CENTER, font=("Roboto", 24))
        enter_name_label.pack(pady=10, padx=10)

        username_entry = customtkinter.CTkEntry(App.frames['page1'], bg_color='#2c2f3c', border_width=1, placeholder_text="Username")
        username_entry.pack(pady=10, padx=10)

        def handle_enter_button(event=None):
            App.username = username_entry.get()
            if App.username is None:
                print("Username cannot be empty!")

        username_entry.bind('<Return>', handle_enter_button)

        enter_button = customtkinter.CTkButton(App.frames['page1'], fg_color='#26c281', hover_color='#4183d7', text="Login", command=handle_enter_button)
        enter_button.pack(pady=10, padx=10)
        

    def get_username(self):
        while App.username is None:
            time.sleep(1)
        return App.username
    
    
    def get_new_message(self):
        while App.new_message is None:
            time.sleep(1)
        return App.new_message
    

    def add_members(self, username):
        each_member_container = customtkinter.CTkFrame(App.member_container, fg_color=Constdata["BACKGROUND_COLOR"], corner_radius=5)
        each_member_container.pack(padx=10, pady=5, fill=tkinter.X)

        member_label = customtkinter.CTkLabel(each_member_container, text=username, font=("Roboto", 13))
        member_label.pack(padx=13, pady=5, anchor="w", side="top")

    
    def add_message(self, username, content):
        if len(App.chat_container.winfo_children()) == 100:
            first_widget = App.chat_container.winfo_children()[0]
            first_widget.destroy()

        MAX_WIDTH = 400

        each_message_container = customtkinter.CTkFrame(App.chat_container, fg_color=Constdata["OTHER_TEXT_COLOR"] if username != App.username else Constdata['MY_TEXT_COLOR'], corner_radius=8, width=MAX_WIDTH)
        each_message_container.pack(padx=10, pady=5, anchor="w" if username != App.username else "e")

        message_text = customtkinter.CTkLabel(each_message_container, text=f'[{username}]: {content}', font=("Roboto", 12), wraplength=MAX_WIDTH-10)
        message_text.pack(padx=13, pady=5, anchor="e", side="top")



    def chatting_page(self):
        # -------------------------------------------member container------------------------------------------------
        member_title = customtkinter.CTkLabel(App.member_container, text="Chat Members")
        member_title.pack(padx=10, pady=10)
        # -------------------------------------------member container------------------------------------------------

        # -------------------------------------------chat title container------------------------------------------------
        chat_title_container = customtkinter.CTkFrame(App.frames['page2'], fg_color=Constdata["BACKGROUND_COLOR"])
        chat_title_container.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        title_label = customtkinter.CTkLabel(chat_title_container, text="This chatting service is well encrypted.", font=("Roboto", 14))
        title_label.pack(padx=10, pady=10, side=tkinter.LEFT)
        # -------------------------------------------chat title container-----------------------------------------------

        # -------------------------------------------input container------------------------------------------------
        input_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#2c2f3c')
        input_container.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        input_container.grid_columnconfigure(0, weight=1000)
        input_container.grid_columnconfigure(1, weight=1)

        input_box = customtkinter.CTkEntry(input_container, placeholder_text="Type a message here...", border_width=0, fg_color='#2c2f3c', corner_radius=10)
        input_box.grid(padx=(10, 0), pady=(5, 5), column=0, row=0, columnspan=1, sticky="ew")

        logo = Image.open("E:/placement/internship SAG/project/sent.png")
        send_logo = customtkinter.CTkImage(dark_image=logo, light_image=logo, size=(20,20))

        def handle_send_button(event=None):
            App.new_message = input_box.get()
            input_box.delete(0, 'end')
            time.sleep(1)

        input_box.bind('<Return>', handle_send_button)

        send_button = customtkinter.CTkButton(input_container, text="", image=send_logo, width=25, fg_color=Constdata["MY_TEXT_COLOR"], command=handle_send_button)
        send_button.grid(padx=(0, 10), pady=(5, 5), column=14, row=0, columnspan=1)

        
        # -------------------------------------------input container------------------------------------------------

        # Configure the grid to ensure proper resizing
        App.frames['page2'].grid_columnconfigure(0, weight=1)
        App.frames['page2'].grid_columnconfigure(1, weight=4)
        App.frames['page2'].grid_rowconfigure(0, weight=1)
        App.frames['page2'].grid_rowconfigure(1, weight=30)
        App.frames['page2'].grid_rowconfigure(2, weight=2)
        

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
        
        App.username = None
        App.new_message = None

        App.member_container = customtkinter.CTkScrollableFrame(App.frames['page2'], fg_color='#2c2f3c')
        App.member_container.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        App.chat_container = customtkinter.CTkScrollableFrame(App.frames['page2'], fg_color=Constdata["BACKGROUND_COLOR"], )
        App.chat_container.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
