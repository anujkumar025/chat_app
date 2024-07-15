# Secure Chat Application

This is a secure chat application built using Python. It utilizes a client-server model to facilitate encrypted communication between users. The application employs asymmetric and symmetric cryptography to ensure the security and confidentiality of messages. The user interface is created using customtkinter, providing a modern and user-friendly experience.

## Features

- Secure communication using asymmetric and symmetric encryption
- User-friendly interface built with customtkinter
- Real-time messaging between clients
- Secure handshake process to establish encrypted communication channels

## Prerequisites

- Python 3.12.0

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/anujkumar025/chat_app.git
```

### Step 2: Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Server

On the device you want to use as the server, run the following command:
and there is no need for other files in this device

```bash
python server.py
```

### Step 4: Network Configuration

Ensure that all devices (client and server) are connected to the same network or WiFi.
Replace Host address in client.py with the ipv4 address of the server  
ipv4 address of a device can be found using ipconfig command

### Step 5: Run the Client

On any other device connected to the same network, run the following command:
all the files other than server.py should be this device

```bash
python client.py
```

## Usage

1. **Start the Server**: Begin by running `server.py` on the server device. The server will start listening for incoming connections from clients.

2. **Start the Client**: Run `client.py` on the client device. The client will prompt the user to enter a username and then connect to the server.

3. **Handshake Process**: The client and server will perform a handshake process to securely exchange a session key. This key will be used for encrypting and decrypting messages.

4. **Send Messages**: After the handshake process, clients can send and receive messages securely. Messages will be encrypted using the session key to ensure privacy.

## Project Structure

- `server.py`: Contains the server-side code for handling client connections and managing encrypted communication.
- `client.py`: Contains the client-side code for connecting to the server, performing the handshake, and sending/receiving messages.
- `requirements.txt`: Lists the required Python packages for the project.
- `README.md`: This file, providing an overview and setup instructions for the project.

## Dependencies

The application requires the following Python packages:

- `customtkinter`
- `cryptography`
- `socket`
- `pickle`

You can install these dependencies using the command provided in the setup steps.

## Notes

- This application is designed to work within a local network. Ensure that all devices are connected to the same WiFi or network for proper functionality.
- The security of the application relies on the proper exchange and handling of cryptographic keys. Ensure that the initial handshake process is completed without interruption for secure communication.

---

With this setup, you should be able to run the secure chat application on devices connected to the same network, ensuring secure and encrypted communication between clients.
