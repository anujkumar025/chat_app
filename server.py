import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from Crypto.Util.Padding import pad, unpad
import pickle 
import os
from Crypto.Cipher import AES


HOST = '127.0.0.1'
PORT = 8081
LISTENER_LIMIT = 5
active_clients = [] # list of all currently connected users
active_user = [] # list of usernames of currently connected users

# generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# generate publick key
public_key = private_key.public_key()
public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )


def decrypt_cipher_text(encrypted_message, SESSION_KEY):
    iv = encrypted_message['iv']
    ciphertext = encrypted_message['ciphertext']

    # Decrypt the message using the session key
    cipher = AES.new(SESSION_KEY, AES.MODE_CBC, iv)
    decrypted_serialized_object = unpad(cipher.decrypt(ciphertext), AES.block_size)
    message = pickle.loads(decrypted_serialized_object)
    return message


def send_messages_to_all(client, raw_data, SESSION_KEY):
    global active_clients, active_user
    decrypted_data = None
    if 'iv' in raw_data.keys():
        decrypted_data = decrypt_cipher_text(raw_data, SESSION_KEY)
    else:
        decrypted_data = raw_data
    
    for user in active_clients:
        if client != user['client']:
            encrypted_data = encrypt_data(decrypted_data, user['session_key'])
            user['client'].sendall(encrypted_data)


def handle_new_user(client, SESSION_KEY):
    global active_clients, active_user
    data_to_send = {
        "title": "essential_data",
        "user_list": active_user
    }
    for user in active_clients:
        encrypted_data = encrypt_data(data_to_send, user['session_key'])
        temp_data = pickle.loads(encrypted_data)
        temp_data['title'] = "essential_data"
        encrypted_data = pickle.dumps(temp_data)
        user['client'].sendall(encrypted_data)


def encrypt_data(data, SESSION_KEY):
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


def return_session_key(client):
    global active_clients, active_user
    selected_obj = None
    for obj in active_clients:
            if obj["client"] == client:
                selected_obj = obj
    return selected_obj['session_key']


def delete_user(client):
    global active_clients, active_user
    filtered_active_clients = []
    for d in active_clients:
        if d['client'] == client:
            active_user.remove(d['username'])
        else:
            filtered_active_clients.append(d)
    
    return filtered_active_clients

    

def listen_for_messages(client, username):
    global active_clients, active_user
    while 1:
        try:
            raw_data = client.recv(2048)
            message = pickle.loads(raw_data)
            # print(message)
            if message['title'] == "handshake3":
                encrypted_session_key = message['session_key']
                session_key = private_key.decrypt(
                    encrypted_session_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                for obj in active_clients:
                    if obj["client"] == client:
                        active_user.append(obj['username'])
                        # print(active_user)
                        # print(active_clients)
                        obj.update({"session_key": session_key})
                anouncement_data = {
                    'title':'channel_secure',
                    'username':'SERVER',
                    'content':username + " joined the chat",
                    'user_list':active_user
                    }
                send_messages_to_all(client, anouncement_data, session_key)
                handle_new_user(client, session_key)
                
            elif message['title'] == 'channel_secure':
                send_messages_to_all(client, message, return_session_key(client))
            else:
                print(f"the message send from client {username} is empty")  
        except ConnectionResetError:
            print(f"Client {username} disconnected unexpectedly.")
            client.close()
            active_clients = delete_user(client)
            break

        except Exception as e:
            print(f"An error occured : {e}")
            client.close()
            active_clients = delete_user(client)
            break


def client_handler(client):
    global active_clients, active_user
    #server will listen for client message that will contain the username
    while True:
        try:
            initial_hello = client.recv(2048)
            received_data = pickle.loads(initial_hello)
            username = received_data['username']
            if username != '':
                temp_data = {'username':username,
                            'client':client}
                active_clients.append(temp_data)
                # print(active_clients)
                data_to_send = {'title': "handshake2", 'public_key': public_key_pem}
                updated = pickle.dumps(data_to_send)
                client.sendall(updated)
                threading.Thread(target=listen_for_messages, args=(client, username)).start()
                break
            else:
                print("client username is empty")
                
            threading.Thread(target=listen_for_messages, args=(client, username)).start()

        except ConnectionResetError:
            print(f"Client {username} disconnected unexpectedly.")
            client.close()
            active_clients = delete_user(client)
            break

        except Exception as e:
            print(f"An error occured : {e}")
            client.close()
            active_clients = delete_user(client)
            break



def main():
    #AF.INET : to use IPv4 addresses
    #SOCK_STREAM : for using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Successfully conneted to the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    #this while loop will keep listening to client connections
    while(1):
        client, address = server.accept()
        print(f"successfully connected to client { address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()