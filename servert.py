import socket
import random

# Define and shuffle a deck of cards
deck = [f"{rank} of {suit}" for suit in ["Hearts", "Diamonds", "Clubs", "Spades"] 
        for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]

# Function to shuffle and reset the deck
def reset_deck():
    global deck
    deck = [f"{rank} of {suit}" for suit in ["Hearts", "Diamonds", "Clubs", "Spades"] 
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]
    random.shuffle(deck)

reset_deck()

# Function to draw a card and remove it from the deck
def draw_card():
    if deck:  # Check if deck is not empty
        return deck.pop()
    else:
        return "No more cards in the deck"

# Function to get the Blackjack value of a card
def get_card_value(card):
    rank = card.split()[0]  # Extract rank (e.g., "Ace", "10", "King")
    if rank in ["Jack", "Queen", "King"]:
        return 10
    elif rank == "Ace":
        return 11
    else:
        return int(rank)

# Function to adjust for Aces if needed
def adjust_for_aces(total, cards):
    while total > 21 and "Ace" in [card.split()[0] for card in cards]:
        total -= 10
        cards.remove(next(card for card in cards if "Ace" in card))
    return total

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))
server.listen(5)
print("Waiting for players to connect...")

# Accept first player
client1, addr1 = server.accept()
print(f"Player 1 connected from {addr1}")
client1.send("What is your name?".encode())
name1 = client1.recv(1024).decode().strip()
print(f"Player 1's name: {name1}")

while True:  # Loop for repeated games
    reset_deck()
    client1.send("You're Player 1. Type 'start' to begin the game.".encode())
    choice = client1.recv(1024).decode().strip().lower()

    if choice == "start":
        client1.send("Game is starting now...".encode())
        print(f"{name1} has started the game!")

        # Deal two initial cards to the player and dealer
        player_cards = [draw_card(), draw_card()]
        dealer_cards = [draw_card(), draw_card()]
        player_total = sum(get_card_value(card) for card in player_cards)
        dealer_total = sum(get_card_value(card) for card in dealer_cards)

        player_total = adjust_for_aces(player_total, player_cards)
        dealer_total = adjust_for_aces(dealer_total, dealer_cards)

        # Send initial card info to the player
        client1.send(f"Your cards: {', '.join(player_cards)}. Total: {player_total}\n"
                     f"Dealer shows: {dealer_cards[0]} (Hidden card not revealed)\n"
                     "Would you like to 'hit' or 'stand'?".encode())

        # Player's turn
        while player_total < 21:
            client1.send("Would you like to 'hit' or 'stand'?".encode())
            choice1 = client1.recv(1024).decode().strip().lower()

            if choice1 in ("hit", "h"):
                new_card = draw_card()
                player_cards.append(new_card)
                player_total += get_card_value(new_card)
                player_total = adjust_for_aces(player_total, player_cards)
                client1.send(f"You drew {new_card}. Your total is {player_total}.".encode())
                
                if player_total > 21:
                    client1.send("You busted! Game over.".encode())
                    break  # End the player's turn
            elif choice1 in ("stand", "s"):
                break  # Player chooses to stand and the game proceeds
            else:
                client1.send("Invalid choice. Please type 'hit' or 'stand'.".encode())  # If invalid input is given

        # Dealer's turn
        if player_total <= 21:
            client1.send(f"Dealer's turn. Dealer reveals: {dealer_cards[1]}.\n".encode())
            while dealer_total < 17:
                new_card = draw_card()
                dealer_cards.append(new_card)
                dealer_total += get_card_value(new_card)
                dealer_total = adjust_for_aces(dealer_total, dealer_cards)
                client1.send(f" Dealer draws {new_card}. \nDealer total is {dealer_total}.".encode())
                if dealer_total > 21:
                    client1.send("\nDealer busted! You win!".encode())
                    break

            # Determine the winner
            if player_total <= 21 and dealer_total <= 21:
                if player_total > dealer_total:
                    client1.send(f"You win! Your total: {player_total}, Dealer's total: {dealer_total}.".encode())
                elif player_total < dealer_total:
                    client1.send(f"You lose! Your total: {player_total}, Dealer's total: {dealer_total}.".encode())
                else:
                    client1.send(f"It's a tie! Your total: {player_total}, Dealer's total: {dealer_total}.".encode())

    # Ask the player if they want to play again
    client1.send("Do you want to play again? (yes/no)".encode())
    play_again = client1.recv(1024).decode().strip().lower()
    if play_again != "yes":
        client1.send("Thanks for playing! Goodbye!".encode())
        break  # End the loop and close the connection

# Close connection properly
client1.close()
server.close()
