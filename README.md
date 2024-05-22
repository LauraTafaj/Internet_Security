# Internet_Security
# Secure File Transfer Application

This application provides a secure way to transfer files over the internet using end-to-end encryption and integrity verification.

## Features

- End-to-end encryption using AES
- Integrity verification using SHA-256
- Client-server architecture
- Graphical User Interface (GUI) with Tkinter

## Components

### Server
- **config.py:** Configuration settings such as server IP, port, buffer size, and encryption key.
- **encryption.py:** Encryption and hashing functionalities using the AES algorithm and SHA-256 hashing.
- **server.py:** Main server application responsible for receiving files securely.

### Client
- **config.py:** Configuration settings for the client application.
- **encryption.py:** Encryption and hashing functionalities for the client side.
- **client.py:** Main client application responsible for sending files securely.

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Start the server by running `python server.py`.
4. Start the client by running `python client.py`.
5. Use the user interface to select files and send/receive them securely.

## Requirements

- Python 3.x
- tkinter (for GUI)
- cryptography (for encryption)
