import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import pickle
import base64

HOST = 'localhost'
PORT = 8081
LISTENER_LIMIT = 5
active_clients = []  # list of all currently connected users

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Serialize public key to send to client
public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

session_keys = {}

def listen_for_messages(client, username):
    while True:
        message = pickle.loads(client.recv(2048))
        if message['title'] == "handshake3":
            encrypted_session_key = base64.b64decode(message['key'])
            try:
                session_key = private_key.decrypt(encrypted_session_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                session_keys[username] = session_key
                print(f"Session key for {username} successfully decrypted.")
            except Exception as e:
                print(f"Failed to decrypt session key for {username}: {e}")
        elif message != '':
            nonce, ciphertext = message['message'].split('~')
            cipher_aes = AES.new(session_keys[username], AES.MODE_EAX, nonce=base64.b64decode(nonce))
            decrypted_message = unpad(cipher_aes.decrypt(base64.b64decode(ciphertext)), AES.block_size)
            final_msg = decrypted_message.decode()
            send_messages_to_all(final_msg, username)
        else:
            print(f"Empty message received from client {username}")

def send_message_to_client(client, message):
    client.sendall(pickle.dumps({"message": message}))

def send_messages_to_all(message, username):
    for user in active_clients:
        if user[0] != username:
            cipher_aes = AES.new(session_keys[user[0]], AES.MODE_EAX)
            nonce = base64.b64encode(cipher_aes.nonce).decode()
            ciphertext = base64.b64encode(cipher_aes.encrypt(pad(message.encode(), AES.block_size))).decode()
            send_message_to_client(user[1], nonce + '~' + ciphertext)

def client_handler(client):
    while True:
        initial_hello = client.recv(2048)
        received_data = pickle.loads(initial_hello)
        username = received_data['username']
        if username != '':
            active_clients.append((username, client))
            client.sendall(pickle.dumps({"title": "handshake2", "public_key": public_key_pem.decode()}))
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Server started on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
