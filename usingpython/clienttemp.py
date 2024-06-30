import socket
import threading
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import pickle
import base64
from Crypto.Random import get_random_bytes

SALT = b'x\xd9\x8b\xefH\x95\x04-\xc5\xe2\xc5\x02Q\xa2\x07L%\xde\xfbk}\xf3\xae\x9f\xf3\x10\xa0\xf1\x9e\x1f^\xd1\xb6\xeb\xbf\xf0h\x98\xcd\xb6\xc7\x0b\xf9\xa8(\x1c?\xe6\xf5\x0b\x00b\x80\xee"\x90\xa77\xb0\x0b+W\xb1\xc4'
password = "xcvksud"
key = PBKDF2(password, SALT, dkLen=32)  # 32 bytes for AES-256

HOST = 'localhost'
PORT = 8081

session_key = None

def listen_for_messages_from_server(client):
    global session_key
    while True:
        message = client.recv(2048)
        data = pickle.loads(message)
        if data['title'] == "handshake2":
            server_public_key = RSA.import_key(data['public_key'])
            cipher_rsa = PKCS1_OAEP.new(server_public_key)
            encrypted_session_key = cipher_rsa.encrypt(session_key)
            client.sendall(pickle.dumps({"title": "handshake3", "key": base64.b64encode(encrypted_session_key).decode()}))
        elif message != '':
            nonce, ciphertext = data['message'].split('~')
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=base64.b64decode(nonce))
            decrypted_message = unpad(cipher_aes.decrypt(base64.b64decode(ciphertext)), AES.block_size)
            username, content = decrypted_message.decode().split('~')
            print(f"[{username}]: {content}")
        else:
            print("Received empty message from server")

def send_message_to_server(client, username):
    while True:
        message = input()
        if message != '':
            data = username + '~' + message
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            nonce = base64.b64encode(cipher_aes.nonce).decode()
            ciphertext = base64.b64encode(cipher_aes.encrypt(pad(data.encode(), AES.block_size))).decode()
            client.sendall(pickle.dumps({"message": nonce + '~' + ciphertext}))
        else:
            print("Empty message")

def communicate_to_server(client):
    global session_key
    username = input("Enter username: ")
    if username != '':
        initial_hello = {"username": username, "message": "hello"}
        serialized_data = pickle.dumps(initial_hello)
        client.sendall(serialized_data)
        session_key = get_random_bytes(32)  # AES-256 session key
    else:
        print("Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_message_to_server(client, username)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print(f"Connected to the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to connect to server {HOST} {PORT}: {e}")
        return

    communicate_to_server(client)

if __name__ == '__main__':
    main()
