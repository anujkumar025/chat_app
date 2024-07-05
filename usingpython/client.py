import socket
import threading
import random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import os

SALT = random.randbytes(64)
# print(SALT)
# SALT = b'x\xd9\x8b\xefH\x95\x04-\xc5\xe2\xc5\x02Q\xa2\x07L%\xde\xfbk}\xf3\xae\x9f\xf3\x10\xa0\xf1\x9e\x1f^\xd1\xb6\xeb\xbf\xf0h\x98\xcd\xb6\xc7\x0b\xf9\xa8(\x1c?\xe6\xf5\x0b\x00b\x80\xee"\x90\xa77\xb0\x0b+W\xb1\xc4'
password = "xcvksud"
SESSION_KEY = PBKDF2(password, SALT, dkLen=32)
# cipher = AES.new(SESSION_KEY, AES.MODE_CBC)
message_list = [] 
member_list = []


HOST = '127.0.0.1'
# HOST = '127.0.0.1'
PORT = 8081

def decrypt_cipher_text(encrypted_message):
    iv = encrypted_message['iv']
    ciphertext = encrypted_message['ciphertext']

    # Decrypt the message using the session key
    cipher = AES.new(SESSION_KEY, AES.MODE_CBC, iv)
    decrypted_serialized_object = unpad(cipher.decrypt(ciphertext), AES.block_size)
    message = pickle.loads(decrypted_serialized_object)
    if len(message["user_list"]) > len(member_list):
        member_list = message["user_list"]
    message_list.append((member_list.index(message['username']), message['content']))
    print(f"[{message['username']}]: {message['content']}") 


def listen_for_messages_from_server(client):
    while 1:
        raw_data = client.recv(2048)
        message = pickle.loads(raw_data) 
        if message['title'] == "handshake2":
            public_key_pem = message['public_key']
            public_key = serialization.load_pem_public_key(public_key_pem)
            encrypted_session_key = public_key.encrypt(
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
        elif message['title'] == 'channel_secure':
           decrypt_cipher_text(message)
        else:
            print("message recieved from client is empty")


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


def send_message_to_server(client, username):
    while 1:
        message = input()
        message_list.append((0, message))
        if message != '':
            data_object = {'title':'channel_secure',
                           'username':username,
                        'content':message}
            serialized_encrypted_data = encrypt_data(data_object)
            client.sendall(serialized_encrypted_data)
        else:
            print("Empty message")
            exit(0)



def communicate_to_server(client):
    username = input("Enter username : ")
    if username != '':
        initial_hello = {"username": username,
                         "message": "hello"}
        serialized_data = pickle.dumps(initial_hello)
        client.sendall(serialized_data)
    else:
        print("username cannot be empty")
        exit(0)
    
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    send_message_to_server(client, username)


def client_main():
    # root.mainloop()

    print("yoyo")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    communicate_to_server(client)

    return [member_list, message_list]