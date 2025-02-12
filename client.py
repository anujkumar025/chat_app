import socket
import threading
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import os
from frontend import App
import time

SALT = os.urandom(64)
password = "xcvksud"
SESSION_KEY = PBKDF2(password, SALT, dkLen=32)
PUBLIC_KEY_SERVER = None
message_list = []
USERNAME = None
member_list = []
frontend_obj = None
new_message_flag = None  # Event to signal new message


HOST = '127.0.0.1'
PORT = 8081

def send_message_to_server(client, data_object):
    global USERNAME, message_list
    if data_object != {}:
        # print(message_list)
        serialized_encrypted_data = encrypt_data(data_object)
        client.sendall(serialized_encrypted_data)
    else:
        print("Empty message")
        exit(0)

def update_frontend_chatting_page():
    global frontend_obj, member_list, message_list
    frontend_obj.page2_selector()


def frontend_chatting_page(client):
    global member_list, message_list, USERNAME, frontend_obj
    update_frontend_chatting_page()
    last_message = None
    while True:
        temp_data = frontend_obj.get_new_message()
        if temp_data and temp_data != last_message:
            last_message = temp_data
            message_list.append((USERNAME, temp_data))
            data_object = {'title':'channel_secure',
                       'username':USERNAME,
                       'content':temp_data
                       }
            frontend_obj.add_message(USERNAME, temp_data)
            # update_frontend_chatting_page()
            send_message_to_server(client, data_object)


def decrypt_cipher_text(client, encrypted_message):
    global member_list, message_list, frontend_obj, USERNAME
    iv = encrypted_message['iv']
    ciphertext = encrypted_message['ciphertext']

    # Decrypt the message using the session key
    cipher = AES.new(SESSION_KEY, AES.MODE_CBC, iv)
    decrypted_serialized_object = unpad(cipher.decrypt(ciphertext), AES.block_size)
    message = pickle.loads(decrypted_serialized_object)
    if message['title'] == "essential_data":
        new_members = [item for item in message['user_list'] if item not in member_list]
        for item in new_members:
            frontend_obj.add_members(item)
        member_list = message['user_list']
        # update_frontend_chatting_page()
        time.sleep(1)
        # print("title : essential_data")
        # print(member_list)
    
    else:
        if message['username'] == "SERVER":
            new_members = [item for item in message['user_list'] if item not in member_list]
            for item in new_members:
                frontend_obj.add_members(item)
            member_list = message["user_list"]
            frontend_obj.add_message(message['username'], message['content'])
            # print("username : SERVER")
            # print(member_list)

        else:
            message_list.append((message['username'], message['content']))
            frontend_obj.add_message(message['username'], message['content'])
            # update_frontend_chatting_page()
            # print(f"message list : {message_list}")
            # print("decrypt cypher text :")
            # print(message_list)
            


def listen_for_messages_from_server(client):
    while 1:
        raw_data = client.recv(2048)
        message = pickle.loads(raw_data) 
        if message['title'] == "handshake2":
            public_key_pem = message['public_key']
            PUBLIC_KEY_SERVER = serialization.load_pem_public_key(public_key_pem)
            encrypted_session_key = PUBLIC_KEY_SERVER.encrypt(
                SESSION_KEY,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            data_to_send = {'title': "handshake3",
                            'session_key': encrypted_session_key}
            serialized_data = pickle.dumps(data_to_send)
            client.sendall(serialized_data)
        elif message['title'] == "essential_data":
            decrypt_cipher_text(client, message)
        elif message['title'] == 'channel_secure':
            decrypt_cipher_text(client, message)
        else:
            print("message recieved from client is empty.")


def encrypt_data(data):
    # Serialize the data object
    serialized_object = pickle.dumps(data)

    # Encrypt the serialized data object using AES
    iv = os.urandom(16)  # AES block size is 16 bytes
    cipher = AES.new(SESSION_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(serialized_object, AES.block_size))

    # Send the IV and the ciphertext to the server
    encrypted_message = {'title':'channel_secure','iv': iv, 'ciphertext': ciphertext}
    serialized_encrypted_message = pickle.dumps(encrypted_message)
    return serialized_encrypted_message



def communicate_to_server(client):
    global USERNAME
    username = frontend_obj.get_username()
    USERNAME = username
    if username != '':
        initial_hello = {"username": username,
                         "message": "hello"}
        serialized_data = pickle.dumps(initial_hello)
        client.sendall(serialized_data)
    else:
        print("username cannot be empty")
        exit(0)
    
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    frontend_chatting_page(client)


def frontend_thread():
    global frontend_obj
    frontend_obj = App()
    frontend_obj.page1_selector()
    frontend_obj.mainloop()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")


    threading.Thread(target=frontend_thread, args=()).start()
    time.sleep(1)
    communicate_to_server(client)


if __name__ == "__main__":
    main()