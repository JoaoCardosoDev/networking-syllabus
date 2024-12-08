import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 1337

clients_authenticated = {}

def process_request(data, conn, addr):
    try:
        authenticated = clients_authenticated.get(addr, False)

        command, payload = data.split("|", 1)

        if not authenticated:
            if command != "AUTH" and command != "EXIT":
                return "ERROR|Authentication required. Please log in first."

        if command == "ECHO":
            return f"OK|{payload}"
        
        elif command == "TIME":
            return f"OK|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        elif command.startswith("AUTH"):
            _, password = data.split("|", 1)
            if password == "1337":
                clients_authenticated[addr] = True  
                conn.sendall("ACK|AUTH|Success".encode())
                return None
            else:
                conn.sendall("ERROR|AUTH|Invalid password".encode())
                return None
            
        elif command == "EXIT":
            return "OK|Goodbye!"
        
        else:
            return "ERROR|Unknown command"

    except ValueError:
        return "ERROR|Invalid format. Use COMMAND|DATA."

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    print(f"Server listening on {HOST}:{PORT}", flush=True)
    server.listen(2)

    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}", flush=True)

        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    print(f"{addr} shutting connection down.", flush=True)
                    break

                response = process_request(data, conn, addr)
                if response:
                    conn.sendall(response.encode())  # Send response back to client
                print(f"Received: {data} | Responded: {response}", flush=True)

                if data.startswith("EXIT|"):
                    break
