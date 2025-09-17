# Encrypted Command & Control (C2) Framework 📡

An educational project to demonstrate the fundamentals of a Command and Control (C2) server and a corresponding implant for remote administration, with all communication secured by end-to-end encryption.

This framework consists of two main components:
* **`c2_server.py`**: The server component that listens for incoming connections from implants.
* **`implant.py`**: The client component that runs on a target machine, connects back to the server, and awaits commands.



---
## ⚠️ Ethical Disclaimer

This tool is intended for **educational and research purposes only**. It should only be used in a controlled environment and on systems you own and have explicit permission to test. Unauthorized use of this tool on any system is illegal. The author is not responsible for any misuse or damage.

---
## ✨ Features

* **Remote Command Execution**: Send shell commands from the C2 server to be executed on the implant machine.
* **Encrypted Communication**: All traffic between the server and implant is encrypted using the Fernet (AES128-CBC) symmetric encryption scheme.
* **File Transfer**:
    * `download`: Retrieve files from the implant's machine.
    * `upload`: Send files from the server to the implant's machine.
* **Persistent Connection**: The implant will continuously try to reconnect to the C2 server if the connection is lost.

---
## 🛠️ Setup & Usage

### 1. Prerequisites
* Python 3
* The `cryptography` library

### 2. Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your_username/your_repository.git](https://github.com/your_username/your_repository.git)
    cd your_repository
    ```
2.  Install the required library:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Generate Encryption Key
Before running, you must generate a secret key that both the server and implant will share.
1.  Run the following command in your terminal:
    ```bash
    python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```
2.  Copy the generated key.
3.  Paste this key into the `ENCRYPTION_KEY` variable in both `c2_server.py` and `implant.py`.

### 4. Running the Framework
1.  **Start the Server**: On your machine, run the C2 server. It will wait for a connection.
    ```bash
    python3 c2_server.py
    ```
2.  **Configure and Run the Implant**:
    * Open `implant.py` and change the `C2_HOST` variable to the IP address of your server machine.
    * Run the implant on your target test machine (e.g., your own VM).
    ```bash
    python3 implant.py
    ```
3.  **Send Commands**: Once the implant connects, you can issue commands from the `C2>` prompt in your server terminal.

### Command Examples
* **Execute a shell command:**
    `C2> whoami`
* **Download a file from the implant:**
    `C2> download /etc/passwd local_passwd.txt`
* **Upload a file to the implant:**
    `C2> upload local_file.txt /tmp/remote_file.txt`
* **Exit the session:**
    `C2> exit`
