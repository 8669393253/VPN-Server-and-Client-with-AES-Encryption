import socket
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Encryption/Decryption setup
key = b'1234567890123456'  # 16-byte key
iv = b'1234567890123456'   # 16-byte IV

def decrypt_data(encrypted_data):
    iv = encrypted_data[:16]  # Extract the IV from the encrypted message
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    return decrypted.decode('utf-8')

def handle_client(client_socket):
    print("Connection established. Waiting for data...")
    data = client_socket.recv(1024)
    decrypted_data = decrypt_data(data)
    
    print(f"Decrypted Data: {decrypted_data}")  # Log decrypted request
    
    # Handle the request and forward it to the target website
    lines = decrypted_data.split("\r\n")
    request_line = lines[0]
    method, path, version = request_line.split()

    host = None
    for line in lines:
        if line.startswith("Host:"):
            host = line.split(":")[1].strip()
            break

    if not host:
        print("Host header missing. Invalid request.")
        client_socket.close()
        return

    # Wrap the socket with SSL for HTTPS requests
    try:
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket = ssl.wrap_socket(destination_socket)  # SSL wrapping
        destination_socket.connect((host, 443))  # HTTPS port is 443
        
        # Send the decrypted data to the destination server
        destination_socket.sendall(decrypted_data.encode())

        # Receive the response from the target server
        response = destination_socket.recv(1024)

        # Send the response back to the client
        client_socket.sendall(response)
        print(f"Forwarded response from {host}")
    except Exception as e:
        print(f"Error forwarding request: {e}")
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
    finally:
        destination_socket.close()
        client_socket.close()

def start_vpn_server(host='127.0.0.1', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"VPN Server listening on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_vpn_server()
