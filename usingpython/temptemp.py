import tkinter
import customtkinter

DARK_MODE = "dark"
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
BACKGROUND_COLOR = '#20222c'
OTHER_TEXT_COLOR = '#2c2f3c'
MY_TEXT_COLOR = '#4183d7'
BUTTON_COLOR = '#26c281'
MEMBER_LIST = ['anuj', 'kumar', 'aditya', 'akash', 'ankit']
MESSAGE_LIST = [[0, "Hello"], [1, "Hi"], [2, "yo"]]


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
        member_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#2c2f3c')
        member_container.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
        member_title = customtkinter.CTkLabel(member_container, text="Chat Members")
        member_title.pack(padx=10, pady=10)

        # username_list = ["random", "names"]
        for username in MEMBER_LIST:
            each_member_container = customtkinter.CTkFrame(member_container, fg_color=BACKGROUND_COLOR, corner_radius=5)
            each_member_container.pack(padx=10, pady=5, fill=tkinter.X)

            member_label = customtkinter.CTkLabel(each_member_container, text=username, font=("Roboto", 13))
            member_label.pack(padx=13, pady=5, anchor="w", side="top")

        # -------------------------------------------member container------------------------------------------------

        # -------------------------------------------chat title container------------------------------------------------
        chat_title_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#30222c')
        chat_title_container.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        title_label = customtkinter.CTkLabel(chat_title_container, text="This chatting service is well encrypted", font=("Roboto", 14))
        title_label.pack(padx=10, pady=10, side=tkinter.LEFT)
        # -------------------------------------------chat title container------------------------------------------------

        # -------------------------------------------chat container------------------------------------------------
        chat_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#25222c')
        chat_container.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        # -------------------------------------------chat container------------------------------------------------

        # -------------------------------------------input container------------------------------------------------
        input_container = customtkinter.CTkFrame(App.frames['page2'], fg_color='#30222c')
        input_container.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="ew")

        input_box = customtkinter.CTkEntry(input_container, placeholder_text="Type message here...")
        input_box.pack(padx=0, pady=0, fill=tkinter.X)
        # -------------------------------------------input container------------------------------------------------

        # Configure the grid to ensure proper resizing
        App.frames['page2'].grid_columnconfigure(0, weight=1)
        App.frames['page2'].grid_columnconfigure(1, weight=4)
        App.frames['page2'].grid_rowconfigure(0, weight=1)
        App.frames['page2'].grid_rowconfigure(1, weight=8)
        App.frames['page2'].grid_rowconfigure(2, weight=1)
        

    def __init__(self):
        super().__init__()
        # self.state('withdraw')
        self.title("Chatting Application")
        self.geometry("1000x650+50+50")

        main_container = customtkinter.CTkFrame(self)
        main_container.grid(row=0, column=0)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        App.frames['page1'] = customtkinter.CTkFrame(main_container, fg_color="#20222c")
        App.frames['page1'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        App.frames['page2'] = customtkinter.CTkFrame(main_container, fg_color="#20242c")
        App.frames['page2'].pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        
        # self.page1_selector()
        # self.login_page()
        self.page2_selector()
        self.chatting_page()



a = App()
a.mainloop()