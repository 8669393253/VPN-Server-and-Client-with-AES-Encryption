import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Encryption setup (AES)
key = b'1234567890123456'  # 16-byte key
iv = b'1234567890123456'   # 16-byte IV

cipher = AES.new(key, AES.MODE_CBC, iv)

def encrypt_data(data):
    iv = os.urandom(16)  # Generate a new IV for each message
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + encrypted  # Prepend the IV to the encrypted data for transmission

def vpn_client_send_data(data, host='127.0.0.1', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    encrypted_data = encrypt_data(data)
    client_socket.sendall(encrypted_data)

    response = client_socket.recv(1024)
    print(f"Response from VPN Server: {response.decode()}")  # Print the response from the server
    client_socket.close()

if __name__ == "__main__":
    # Specify the website and resource you want to access
    website = "www.google.com"  # You can change this to any website
    path = "/"  # You can change this to any path

    # Prepare the GET request
    data = f"GET {path} HTTP/1.1\r\nHost: {website}\r\n\r\n"
    vpn_client_send_data(data)
