import socket

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect(('localhost', 5000))
print("Connected to server")

# Receive and print the server's first message (asking for name)
server_message = client.recv(1024).decode()
print(server_message)

# Send name to the server
name = input("Enter your name: ")
client.send(name.encode())

# Receive the next server message
server_message = client.recv(1024).decode()
print(server_message)

# Ask whether to start or wait
choice = input("Enter your choice ('start' or 'wait'): ").strip().lower()
client.send(choice.encode())

# Receive response from the server
response = client.recv(1024).decode()
print(response)

# If the game starts, receive the cards and total value
if choice == "start":
    game_info = client.recv(1024).decode()
    print(game_info)

    # Ask if player wants to hit or stand
    choice1 = input("Enter your choice ('hit' or 'stand'): ").strip().lower()
    client.send(choice1.encode())  # ✅ FIXED: Now sending choice1 instead of choice

    # Receive new game state (after hitting or standing)
    new_game_state = client.recv(1024).decode()
    print(new_game_state)

# Close connection
client.close()
