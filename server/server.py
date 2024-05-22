import socket
import tkinter as tk
from tkinter import filedialog, messagebox
from encryption import Encryptor
from config import SERVER_IP, SERVER_PORT, BUFFER_SIZE, ENCRYPTION_KEY

class FileTransferServer:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure File Transfer - Server")
        self.master.configure(bg='black')

        self.encryptor = Encryptor(ENCRYPTION_KEY)

        self.save_path = tk.StringVar()

        tk.Label(master, text="Secure File Transfer", fg='white', bg='black', font=("Arial", 16)).pack(pady=10)
        tk.Entry(master, textvariable=self.save_path, width=50, fg='black', bg='grey').pack(pady=10)
        tk.Button(master, text="Browse", command=self.browse_location, fg='white', bg='grey').pack(pady=10)
        tk.Button(master, text="Receive File", command=self.receive_file, fg='white', bg='grey').pack(pady=10)

    def browse_location(self):
        self.save_path.set(filedialog.askdirectory())

    def receive_file(self):
        save_path = self.save_path.get()
        if not save_path:
            messagebox.showwarning("No save location selected", "Please select a location to save the received file")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', SERVER_PORT))
                s.listen()
                print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")

                    # Receive encrypted data length
                    data_length = int(conn.recv(16).decode().strip())
                    encrypted_data = b''
                    while len(encrypted_data) < data_length:
                        packet = conn.recv(BUFFER_SIZE)
                        if not packet:
                            break
                        encrypted_data += packet

                    # Receive hash
                    received_hash = conn.recv(32)  # SHA-256 hash size

                    data = self.encryptor.decrypt(encrypted_data)
                    calculated_hash = self.encryptor.hash(data)

                    if received_hash == calculated_hash:
                        file_path = filedialog.asksaveasfilename(initialdir=save_path, title="Save File As")
                        with open(file_path, 'wb') as file:
                            file.write(data)
                        messagebox.showinfo("Success", "File received and verified")
                    else:
                        messagebox.showerror("Error", "Data integrity check failed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to receive file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferServer(root)
    root.mainloop()
