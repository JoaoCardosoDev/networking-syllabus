import socket
import time

HOST = "python_server"
PORT = 1337

def client():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print("Connected to the server. Type 'exit' to quit.")
                
                while True:
                    command = input("Enter command (AUTH, ECHO|, TIME|, EXIT|): ").strip()

                    if command.lower() == "exit":
                        s.sendall(b"EXIT|")
                        print("Closing connection.")
                        break
                    elif command == "AUTH":
                        password = input("Enter password: ")
                        message = f"AUTH|{password}"
                        s.sendall(message.encode())
                    else:
                        s.sendall(command.encode())

                    response = s.recv(1024).decode()
                    print(f"Server response: {response}")

                    # Handle specific response types
                    if "Goodbye" in response:
                        print("Server acknowledged exit, closing client.")
                        break
                break
        except ConnectionRefusedError:
            print("Connection refused, retrying in 1 second...", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    client()
