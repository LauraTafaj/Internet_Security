import socket
import tkinter as tk
from tkinter import filedialog, messagebox
from encryption import Encryptor
from config import SERVER_IP, SERVER_PORT, BUFFER_SIZE, ENCRYPTION_KEY

class FileTransferClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure File Transfer - Client")
        self.master.configure(bg='black')

        self.encryptor = Encryptor(ENCRYPTION_KEY)

        self.file_path = tk.StringVar()

        tk.Label(master, text="Secure File Transfer", fg='white', bg='black', font=("Arial", 16)).pack(pady=10)
        tk.Entry(master, textvariable=self.file_path, width=50, fg='black', bg='grey').pack(pady=10)
        tk.Button(master, text="Browse", command=self.browse_file, fg='white', bg='grey').pack(pady=10)
        tk.Button(master, text="Send File", command=self.send_file, fg='white', bg='grey').pack(pady=10)

    def browse_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def send_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showwarning("No file selected", "Please select a file to send")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                
                with open(file_path, 'rb') as file:
                    data = file.read()

                encrypted_data = self.encryptor.encrypt(data)
                file_hash = self.encryptor.hash(data)

                # Send the length of encrypted data first
                s.sendall(f"{len(encrypted_data):<16}".encode())
                
                s.sendall(encrypted_data)
                s.sendall(file_hash)
                
                messagebox.showinfo("Success", "File sent successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferClient(root)
    root.mainloop()
