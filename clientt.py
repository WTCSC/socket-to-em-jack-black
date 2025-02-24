import socket

# Connect to the server
server_address = ('localhost', 5000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

try:
    # Receive and display the initial message
    message = client.recv(1024).decode()
    print(message)

    # Send player's name
    name = input("Enter your name: ")
    client.send(name.encode())

    # Receive and display the game start or wait message
    message = client.recv(1024).decode()
    print(message)

    # Decide to start the game
    if 'Type' in message:
        choice = input("Type 'start' to begin the game: ")
        client.send(choice.encode())

    while True:
        message = client.recv(1024).decode()
        print(message)
        if 'hit' in message.lower() or 'stand' in message.lower():
            choice = input("Type 'hit' or 'stand': ")
            client.send(choice.encode())
        elif 'game over' in message.lower() or 'win' in message.lower() or 'lose' in message.lower() or 'tie' in message.lower():
            break

finally:
    print("Closing connection...")
    client.close()
