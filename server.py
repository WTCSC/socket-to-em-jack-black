import socket
import random

# Define a deck of cards
deck = [f"{rank} of {suit}" for suit in ["Hearts", "Diamonds", "Clubs", "Spades"] 
        for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]

# Function to draw a card and remove it from the deck
def draw_card():
    if deck:  # Check if deck is not empty
        return deck.pop(random.randint(0, len(deck) - 1))
    else:
        return "No more cards in the deck"

# Function to get the Blackjack value of a card
def get_card_value(card):
    rank = card.split()[0]  # Extract rank (e.g., "Ace", "10", "King")
    if rank in ["Jack", "Queen", "King"]:
        return 10
    elif rank == "Ace":
        return 11  # Default to 11 (adjust later if needed)
    else:
        return int(rank)

game_start = 0
player_total = 0  # Track total value of player's cards

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to 0.0.0.0:5000
server.bind(('0.0.0.0', 5000))

# Listen for connections
server.listen(5)
print("Waiting for players to connect...")

# Accept first player
client1, addr1 = server.accept()
print(f"Player 1 connected from {addr1}")

# Ask Player 1 for their name
client1.send("What is your name?".encode())
name1 = client1.recv(1024).decode().strip()
print(f"Player 1's name: {name1}")

# Ask if they want to start the game or wait
client1.send("You're Player 1. Type 'start' to begin the game or 'wait' to wait for more players.".encode())
choice = client1.recv(1024).decode().strip().lower()

if choice == "start":
    game_start += 1
    client1.send("Game is starting now...".encode())
    print(f"{name1} has started the game!")

    # Deal two initial cards
    card1 = draw_card()
    card2 = draw_card()
    dealer_visible = draw_card()
    dealer_hidden = draw_card()

    player_total = get_card_value(card1) + get_card_value(card2)

    # Send card info to the player
    client1.send(f"Your cards: {card1}, {card2}. Total value: {player_total}\n"
                 f"The dealer shows: {dealer_visible} (Hidden card not revealed yet)\n"
                 "Would you like to 'hit' or 'stand'?".encode())

    # Receive player's decision
    choice1 = client1.recv(1024).decode().strip().lower()

    if choice1 in ("hit", "h"):
        new_card = draw_card()
        player_total += get_card_value(new_card)
        client1.send(f"You drew {new_card}. Your new total is {player_total}.".encode())

    elif choice1 in ("stand", "s"):
        client1.send(f"You chose to stand. Your total remains {player_total}.".encode())

elif choice == "wait":
    client1.send("Waiting for more players...".encode())
    print(f"{name1} is waiting for more players...")

else:
    client1.send("Invalid choice. Please restart the game.".encode())

# Close connection
client1.close()
server.close()
