import socket
from cryptography.fernet import Fernet

HOST="localhost"
PORT=12657
key=Fernet.generate_key()
with open("file-secret.key","wb") as f:
    f.write(key)

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
server.bind((HOST, PORT))
server.listen(5)
print(f"Listening on {PORT}")
try:
    while True:
        conn, addr = server.accept()
        print(f"Connection rcvd from {addr[0]} on {addr[1]}")
        conn.send(key)
        data=conn.recv(1024)
        if data == "<END>":
            print("Server stop")
            break
        else: 
            print(data.decode())
except KeyboardInterrupt:
    print("KeyBoard Interrupt !!")