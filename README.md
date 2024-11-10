# VPN Server and Client with AES Encryption

This project demonstrates a simple VPN-like system built with Python, which uses **AES encryption** to secure HTTP requests between the client and the server. The client encrypts its requests using AES before sending them over a TCP connection to the server, which then decrypts and forwards the request to a target website. The server's response is then encrypted and sent back to the client.

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
   - [Encryption/Decryption Process](#encryptiondecryption-process)
   - [Server Workflow](#server-workflow)
   - [Client Workflow](#client-workflow)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
   - [Running the Server](#running-the-server)
   - [Running the Client](#running-the-client)
6. [Security Considerations](#security-considerations)
7. [Future Improvements](#future-improvements)

## Overview

This project consists of two main Python scripts:

1. **VPN Server**: Listens for incoming encrypted HTTP requests, decrypts them, forwards the requests to a target website, receives the response, and sends it back to the client.
2. **VPN Client**: Encrypts HTTP requests using AES, sends them to the server, and prints the decrypted response from the server.

This simple setup emulates a secure VPN tunnel by encrypting HTTP requests with AES before they are sent over the network.

## How It Works

The system uses **AES encryption** in **CBC mode** to ensure confidentiality of the HTTP requests. Both the client and server communicate over a TCP socket, and SSL is used for secure communication between the server and the target websites. 

### Encryption/Decryption Process

1. **AES Encryption**:
   - **Key and IV**: Both the client and server use a pre-defined, static 16-byte key and initialization vector (IV) for encryption and decryption. This key and IV are hardcoded in the scripts.
   - **Padding**: Since AES requires data to be a multiple of its block size (16 bytes), the data is padded using **PKCS7** padding before encryption.
   - **Encryption**: The client generates a new random IV for each request, encrypts the HTTP request data with this IV using AES in CBC mode, and prepends the IV to the encrypted data.
   
2. **AES Decryption**:
   - The server receives the encrypted data, extracts the IV, and uses the same key to decrypt the message using AES in CBC mode. After decryption, the data is unpadded, and the plaintext HTTP request is retrieved.

### Server Workflow

1. **Listening for Client Connections**:
   - The VPN server listens for incoming TCP connections on a specified port (default is 9999).
   - Upon receiving a connection, the server reads the incoming encrypted data.

2. **Decryption**:
   - The server extracts the IV from the encrypted data and uses the same AES key and IV to decrypt the data.
   - After decrypting, it splits the data into an HTTP request and identifies the `Host:` header to determine the target server.

3. **Forwarding the Request**:
   - The server establishes an **SSL connection** to the target server (on port 443) and forwards the decrypted HTTP request.
   - It receives the response from the target server and sends it back to the client.

4. **Error Handling**:
   - If there is an issue (e.g., no `Host:` header in the request or connection failures), the server sends a `500 Internal Server Error` response to the client.

### Client Workflow

1. **Preparing the Request**:
   - The client constructs a simple **HTTP GET request** (by default, for `www.google.com`).
   
2. **Encryption**:
   - Before sending the request, the client encrypts it using AES in CBC mode. A new IV is generated for each request to ensure the encrypted data is unique.

3. **Sending the Request**:
   - The encrypted HTTP request is sent to the server over a TCP connection.

4. **Receiving and Printing the Response**:
   - The client waits for the server's response, decrypts it, and prints it to the console.

## Requirements

- **Python 3.x** (preferably 3.7+)
- Python dependencies:
  - `pycryptodome` for AES encryption:

  - pip install pycryptodome
  

## Installation

1. **Clone or Download** the repository containing the `vpn_server.py` and `vpn_client.py` scripts.

2. **Install dependencies**:
   - Run the following command to install the necessary Python package:
  
pip install pycryptodome


## Usage

### Running the Server

1. **Start the VPN server** by running the following command:

python vpn_server.py

The server will start listening on `127.0.0.1:9999` for incoming client connections.

### Running the Client

1. **Start the VPN client** by running the following command:
  
python vpn_client.py

   - By default, the client sends a GET request to `www.google.com`.
   - The client encrypts the request, sends it to the server, and prints the decrypted response.

## Security Considerations

While this project demonstrates the basic concept of encrypting HTTP requests using AES, there are several security concerns that need to be addressed for real-world implementations:

1. **Hardcoded Keys and IVs**:
   - The encryption key and IV are hardcoded in the scripts, which is not secure. In a production environment, you should use secure key exchange methods (e.g., Diffie-Hellman) to exchange encryption keys between the client and server.
   
2. **No Authentication**:
   - The current system does not include any authentication or integrity checks, which means that an attacker could potentially forge requests or modify the data in transit.
   
3. **Lack of SSL/TLS for Client-Server Communication**:
   - The communication between the client and server is not encrypted with SSL/TLS. In a production setting, you should use SSL/TLS for the communication between the client and server to protect against MITM (Man-In-The-Middle) attacks.
   
4. **IV Reuse**:
   - While the client generates a new IV for each request, reusing the same IV across multiple requests could lead to security vulnerabilities. Ensure the IV is random and unique for each encryption operation.

## Future Improvements

1. **Key Exchange**:
   - Implement a secure key exchange protocol (e.g., Diffie-Hellman or RSA) to securely share encryption keys between the client and server.

2. **SSL/TLS for Client-Server Communication**:
   - Wrap the communication between the client and server in SSL/TLS to ensure that the initial request and response are encrypted, even before applying AES encryption.

3. **Authentication and Integrity**:
   - Introduce authentication (e.g., using HMAC) to ensure that only authorized clients can connect to the server.
   - Add integrity checks to ensure that the data hasn't been tampered with during transmission.

4. **Support for More HTTP Methods**:
   - Currently, the client sends a hardcoded GET request. Extend the client to support other HTTP methods (POST, PUT, DELETE, etc.).

5. **Improved Error Handling**:
   - Enhance error handling on both the client and server sides, including more descriptive error messages and handling timeouts and retries.
     
