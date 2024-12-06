import socket
import time

HOST = "python_server"
PORT = 1337 

def client():
    # KEY=123
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # s.sendall(KEY)
                s.sendall(b"Hello, server!")
                data = s.recv(1024)
                print(f"Received from server: {data.decode()}", flush=True) 
                break  
        except ConnectionRefusedError:
            print("Connection refused, retrying in 1 second...", flush=True)
            time.sleep(1)  

if __name__ == "__main__":
    client()