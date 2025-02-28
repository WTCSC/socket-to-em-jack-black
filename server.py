import socket #imports socket so we can set up the server and client connection
import random #imports random so we can get random cards for both the player and the dealer

currency = 100
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
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5000)) #sets up our socket and uses port 5000
server.listen(5) 
print("Waiting for players to connect...")


#Accept  player
client1, addr1 = server.accept() #accepts a client to join
print(f"Player connected from {addr1}") #prints player connected
client1.send("What is your name?".encode()) #asks for the players name
name1 = client1.recv(1024).decode().strip() #takes in what the client entered and cleans it
print(f"Player name: {name1}") #returns the players name


try: #starts our try to handle any errors the raise
    while True:  #Loops for multiple games
        reset_deck() #resets our deck before the game starts
        client1.send("Type 'start' to begin the game.".encode()) #tells the player to type start to start the game
        choice = client1.recv(1024).decode().strip().lower() #takes in what the client entered and cleans it, looking for start to be entered


        if choice == "start": #if the client does enter start
            #client1.send("Game is starting now...".encode()) #sends the game is starting
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
                #client1.send("Would you like to 'hit' or 'stand'?".encode())
                choice1 = client1.recv(1024).decode().strip().lower() #Decodes and cleans up the response from the client

                if choice1 in ("hit", "h"): #If their response is hit
                    new_card = draw_card() #sets up using the new card variable to the draw card function to get random cards for our new cards
                    player_cards.append(new_card) #Appends the new card to the player_cards dictionary
                    player_total += get_card_value(new_card) #Player total addes the new_card using our get_card_value function
                    player_total = adjust_for_aces(player_total, player_cards) #Adjusts the player total if the player has aces and their score is over 21, adjusts aces from 11 to 1
                    client1.send(f"You drew {new_card}. Your total is {player_total}.".encode()) #Sends that the player drew a new card, and displays what it is, then displays our player total
                    
                    if player_total > 21: #of player total score is greater than 21
                        currency = currency/2 #take their currency and divide it by 2 because they lost
                        client1.send(f"You busted! Game over, You have {currency} Dollars.".encode()) #tells the player that they busted. and then displays their new currency value
                        break  # End the player's turn #break this loop since the player lost
                elif choice1 in ("stand", "s"): #if the player chooses to stand, break the players turn loop
                    break  # Player chooses to stand and the game proceeds
                else:
                    client1.send("Invalid choice. Please type 'hit' or 'stand'.".encode())  #If the player inputs something other than hit or stand, we respond that their input was invalid

            # Dealer's turn
            if player_total <= 21: #if player total is less than or equal to 21, the dealer plays
                client1.send(f"Dealer's turn. Dealer reveals: {dealer_cards[1]}.\n".encode()) #sends that its the dealers turn
                while dealer_total < 17: #if the dealer has anything less than 17
                    new_card = draw_card() #mew card using our draw card function
                    dealer_cards.append(new_card) #appends the new card to the dealers card list
                    dealer_total += get_card_value(new_card) #dealer total plus their new card
                    dealer_total = adjust_for_aces(dealer_total, dealer_cards) #Adjust for aces if the dealer has more than 21 and has aces
                    client1.send(f" Dealer draws {new_card}. \nDealer total is {dealer_total}.".encode()) #Prints and sends that the dealer drew a card and their new total
                    if dealer_total > 21: #if the dealer has more than 21 and the player is still in(which the player has to be if we get this far)
                        currency = currency*2 #the dealer loses and the player wins, doubling their currency.
                        client1.send(f"\nDealer busted! You win! You have {currency} Dollars.".encode()) #Prints and sends that the dealer busted and that the player won and their new currency value
                        break

                # Determine the winner
                if player_total <= 21 and dealer_total <= 21: #if both code submit, and both are less than or equal to 21
                    if player_total > dealer_total: #if the player has a higher score
                        currency = currency*2 #double the players currency
                        client1.send(f"You win! Your total: {player_total}, Dealer's total: {dealer_total}, You have {currency} Dollars.".encode()) #prints that the player won, they score, dealers score, and their currency.
                    elif player_total < dealer_total: #if the players score is less than the dealers score
                        currency = currency/2 #player lost so their currency gets divided by 2
                        client1.send(f"You lose! Your total: {player_total}, Dealer's total: {dealer_total}, You have {currency} Dollars..".encode()) #prints that the player lost, their score, dealers score, and their currency
                    else:
                        currency = currency #currency stays the same because it was a tie
                        client1.send(f"It's a tie! Your total: {player_total}, Dealer's total: {dealer_total}, You have {currency} Dollars..".encode()) #prints that it was a tie, player score, dealer score and their currency.

    # Ask the player if they want to play again
        client1.send("Do you want to play again? (yes/no)".encode()) #Asks the player after a game if they would like to play again.
        play_again = client1.recv(1024).decode().strip().lower() #decodes the answer of the player and cleans it up

        if "no" in play_again: #if no in play again, (player response)
            client1.send("Thanks for playing! Goodbye!".encode()) #Send thanks for playing and goodbye to the player
            break  #End the loop and close the connection 
        elif "yes" in play_again: #of yes in player response, continue, restarts the game with loop
            continue  #Restart the game loop

except BrokenPipeError: #excepts broken pipe error if data doesn't make it
    print("Connection to client severed") #prints connection to client was severed
except KeyboardInterrupt: #excepts keyboardInterrupt error if code is haulted
    print("Shutting down server") #Shuts down server for keyboard interrupt
except Exception as e: #For anything we don't specify as an error 
    print(f"Server error: {e}")#Prints "Client error: "
finally: #establishes what we do once failed
    client1.close() #close client
    server.close() #close server
    print("Server closed.") #print server closed.