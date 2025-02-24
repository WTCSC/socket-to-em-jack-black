import socket

# Start the client
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))
    
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print(data)
        
        if "Goodbye" in data:
            break
        
        message = input("Enter your response: ").strip()
        client.sendall(message.encode())
    
    client.close()
    print("Disconnected from server.")

if __name__ == "__main__":
    start_client()
