from client import client_main
from frontend import App
import threading

MEMBER_LIST = []
MESSAGE_LIST = []

def start_frontend():
    print("yo")
    [MEMBER_LIST, MESSAGE_LIST] = client_main()
    

def main():
    backend_thread = threading.Thread(target=start_frontend, args=())
    backend_thread.start()

    backend_thread.join()
    a = App(MEMBER_LIST, MESSAGE_LIST)
    a.mainloop()
    print("all fine")


if __name__ == "__main__":
    main()
