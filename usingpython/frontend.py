import tkinter
import customtkinter
# from tkinter import PhotoImage
from PIL import Image
from data import Constdata

# DARK_MODE = "dark"
# BACKGROUND_COLOR = '#20222c'
# OTHER_TEXT_COLOR = '#2c2f3c'
# MY_TEXT_COLOR = '#4183d7'
# BUTTON_COLOR = '#26c281'
# MEMBER_LIST = ['anuj', 'kumar', 'bnuj', 'cnuj', 'dnuj']
# MESSAGE_LIST = [[0, "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."], [1, "Hi"], [2, "yo"], [3, "2Hello"], [4, "Hi"], [3, "yo"], [0, "3Hello"], [3, "Hi"], [2, "yo"], [0, "4Hello"], [2, "Hi"], [4, "yo"], [0, "5Hello"], [3, "Hi"], [2, "yo"]]


class App(customtkinter.CTk):

    frames = {"page1": None, "page2": None}

    def page1_selector(self):
        App.frames["page2"].pack_forget()
        App.frames["page1"].pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def page2_selector(self):
        App.frames["page1"].pack_forget()
        App.frames["page2"].pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
    
    def login_page(self):

        enter_name_label = customtkinter.CTkLabel(App.frames['page1'], text="Enter Username", anchor=tkinter.CENTER, font=("Roboto", 24))
        enter_name_label.pack(pady=10, padx=10)

        username_entry = customtkinter.CTkEntry(App.frames['page1'], bg_color='#2c2f3c', border_width=1, placeholder_text="Username")
        username_entry.pack(pady=10, padx=10)

        enter_button = customtkinter.CTkButton(App.frames['page1'], fg_color='#26c281', hover_color='#4183d7', text="Login")
        enter_button.pack(pady=10, padx=10)

    
    def chatting_page(self):
        # -------------------------------------------member container------------------------------------------------
        member_container = customtkinter.CTkScrollableFrame(App.frames['page2'], fg_color='#2c2f3c')
        member_container.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
        member_title = customtkinter.CTkLabel(member_container, text="Chat Members")
        member_title.pack(padx=10, pady=10)

        # username_list = ["random", "names"]
        for username in self.MEMBER_LIST:
            each_member_container = customtkinter.CTkFrame(member_container, fg_color=Constdata["BACKGROUND_COLOR"], corner_radius=5)
            each_member_container.pack(padx=10, pady=5, fill=tkinter.X)

            member_label = customtkinter.CTkLabel(each_member_container, text=username, font=("Roboto", 13))
            member_label.pack(padx=13, pady=5, anchor="w", side="top")

        # -------------------------------------------member container------------------------------------------------

        # -------------------------------------------chat title container------------------------------------------------
        chat_title_container = customtkinter.CTkFrame(App.frames['page2'], fg_color=Constdata["BACKGROUND_COLOR"])
        chat_title_container.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        title_label = customtkinter.CTkLabel(chat_title_container, text="This chatting service is well encrypted", font=("Roboto", 14))
        title_label.pack(padx=10, pady=10, side=tkinter.LEFT)
        # -------------------------------------------chat title container------------------------------------------------

        # -------------------------------------------chat container------------------------------------------------
        chat_container = customtkinter.CTkScrollableFrame(App.frames['page2'], fg_color=Constdata["BACKGROUND_COLOR"], )
        chat_container.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")

        # chat_container.grid_columnconfigure((0, 1, 2), weight=1)

        MAX_WIDTH = 400
        for message in self.MESSAGE_LIST:

            each_message_container = customtkinter.CTkFrame(chat_container, fg_color=Constdata["OTHER_TEXT_COLOR"] if message[0] else Constdata["MY_TEXT_COLOR"], corner_radius=8, width=MAX_WIDTH)
            # each_message_container.grid(column=0 if message[0] else 1, columnspan = 2, sticky="ew", pady=5, padx=5)

            each_message_container.pack(padx=10, pady=5, anchor="w" if message[0] else "e")

            message_text = customtkinter.CTkLabel(each_message_container, text=f'[{self.MEMBER_LIST[message[0]]}]: {message[1]}', font=("Roboto", 12), wraplength=MAX_WIDTH-10)
            message_text.pack(padx=13, pady=5, anchor="e", side="top")
                

        # -------------------------------------------chat container------------------------------------------------

        # -------------------------------------------input container------------------------------------------------
        input_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#2c2f3c')
        input_container.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        input_container.grid_columnconfigure(0, weight=1000)
        input_container.grid_columnconfigure(1, weight=1)

        input_box = customtkinter.CTkEntry(input_container, placeholder_text="Type a message here...", border_width=0, fg_color='#2c2f3c', corner_radius=10)
        input_box.grid(padx=(10, 0), pady=(5, 5), column=0, row=0, columnspan=1, sticky="ew")

        logo = Image.open("E:/placement/internship SAG/project/usingpython/sent.png")
        send_logo = customtkinter.CTkImage(dark_image=logo, light_image=logo, size=(20,20))

        send_button = customtkinter.CTkButton(input_container, text="", image=send_logo, width=25, fg_color=Constdata["MY_TEXT_COLOR"])
        send_button.grid(padx=(0, 10), pady=(5, 5), column=14, row=0, columnspan=1)

        
        # -------------------------------------------input container------------------------------------------------

        # Configure the grid to ensure proper resizing
        App.frames['page2'].grid_columnconfigure(0, weight=1)
        App.frames['page2'].grid_columnconfigure(1, weight=4)
        App.frames['page2'].grid_rowconfigure(0, weight=1)
        App.frames['page2'].grid_rowconfigure(1, weight=30)
        App.frames['page2'].grid_rowconfigure(2, weight=2)

        

    def __init__(self, MEMBER_LIST, MESSAGE_LIST):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        super().__init__()
        # self.state('withdraw')
        self.title("Chatting Application")
        self.geometry("1000x650+50+50")

        main_container = customtkinter.CTkFrame(self)
        main_container.grid(row=0, column=0)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        App.frames['page1'] = customtkinter.CTkFrame(main_container, fg_color=Constdata["BACKGROUND_COLOR"])
        App.frames['page1'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        App.frames['page2'] = customtkinter.CTkFrame(main_container, fg_color=Constdata["BACKGROUND_COLOR"])
        App.frames['page2'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        
        # self.page1_selector()
        # self.login_page()
        self.page2_selector()
        self.chatting_page()