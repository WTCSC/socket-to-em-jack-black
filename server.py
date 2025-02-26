import socket
import random


#We set up our deck of cards with each suit having 13 possibilities of value
deck = [f"{rank} of {suit}" for suit in ["Hearts", "Diamonds", "Clubs", "Spades"] #Suits
        for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]] #Card values



#Function to shuffle and reset the deck
def reset_deck():
    global deck #uses global to reset the deck for all of our code and not just locally
    deck = [f"{rank} of {suit}" for suit in ["Hearts", "Diamonds", "Clubs", "Spades"] 
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]
    random.shuffle(deck)#Shuffles all the cards



reset_deck()

#Function to give us a random card and then remove it, using pop, from the deck
def draw_card(): #draw_card function used by our dealer and by the client(us)
    if deck:  # Check if deck has something in it
        return deck.pop() #return the card we popped out of the deck
    else:
        return "No more cards in the deck" #returns if our deck is empty



#Defining our get card value function so that we can get the value of a card later on to get the score of the player and dealer
def get_card_value(card): #defines function
    rank = card.split()[0]  #Gets rank of card ("Ace", "10", "King")
    if rank in ["Jack", "Queen", "King"]: #if the card is a face, its worth 10
        return 10 #returns 10
    elif rank == "Ace": #if the card is ace, returns 11
        return 11 #returns 11
    else:
        return int(rank) #returns the integar value of the card


#Function that will change the value of an ace if nessesary
def adjust_for_aces(total, cards): #defines our fucntion
    while total > 21 and "Ace" in [card.split()[0] for card in cards]: #If youre score is greater than 21, we subract 10 to make the ace worth 1
        total -= 10 #subtracts 10
        cards.remove(next(card for card in cards if "Ace" in card))
    return total



#Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sets up our socket
server.bind(('0.0.0.0', 5000)) #sets up our socket and uses port 5000
server.listen(5) 
print("Waiting for players to connect...")


#Accept  player
client1, addr1 = server.accept() #accepts a client to join
print(f"Player connected from {addr1}") #prints player connected
client1.send("What is your name?".encode()) #asks for the players name
name1 = client1.recv(1024).decode().strip() #takes in what the client entered and cleans it
print(f"Player name: {name1}") #returns the players name



while True:  #Loops for multiple games
    reset_deck() #resets our deck before the game starts
    client1.send("Type 'start' to begin the game.".encode()) #tells the player to type start to start the game
    choice = client1.recv(1024).decode().strip().lower() #takes in what the client entered and cleans it, looking for start to be entered


    if choice == "start": #if the client does enter start
        client1.send("Game is starting now...".encode()) #sends the game is starting
        print(f"{name1} has started the game!") #game started


        #Deal two initial cards to the player and dealer
        player_cards = [draw_card(), draw_card()] #deals the player their two initial cards
        dealer_cards = [draw_card(), draw_card()] #deals the dealer their two initial cards
        player_total = sum(get_card_value(card) for card in player_cards) #gets the sum of all cards in the players hand to give us the player score/total
        dealer_total = sum(get_card_value(card) for card in dealer_cards) #gets the sum of all cards in the dealers hand to give us the dealer score/total


        player_total = adjust_for_aces(player_total, player_cards) #Adjusts for aces if the player has any 
        dealer_total = adjust_for_aces(dealer_total, dealer_cards) #Adjusts for aces if the dealer has any


        #Send initial cards info to the player
        client1.send(f"Your cards: {', '.join(player_cards)}. Total: {player_total}\n" #prints to the player what their cards are
                     f"Dealer shows: {dealer_cards[0]} (Hidden card not revealed)\n" #prints to the player what the dealer has
                     "Would you like to 'hit' or 'stand'?".encode()) #asks the player if they would like to hit or stand


        #Player's turn
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
