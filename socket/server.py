import socket

HOST = "0.0.0.0"
PORT = 1337
KEY="123"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    print(f"Server listening on {HOST}:{PORT}", flush=True) 
    server.listen(2)

    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}", flush=True)  
        
        with conn:
            while True:
                data = conn.recv(1024)
                # if data.decode() != KEY:
                #     break
                if not data:
                    print(f"{addr} shutting connection down.", flush=True)
                    break
                conn.sendall(data)
                print(data, flush=True)  