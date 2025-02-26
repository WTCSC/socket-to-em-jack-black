# Blackjack server README
## Overview
This is a simple network gameof black jack by using Python. It allows a single player to connect and play against the dealer. 
## Features
- Supports single player
- Uses a shuffled deck of 52
- Uses normal black jack standards like hit, stand, and a money feature
- Dealer hits on 16 and lower and stands on 17+
- Normal black jack rules
## Requirements
- Python 3.x

## How to run the script
1. Open the terminal and run python3 server.py
2. The server should be reader for the client to connect so in a seperate terminal do the command python3 client.py
## How do you play black jack?
The game starts by giving you 2 cards and a number card 2-10 will be EQUAL to its number so example is 8 is equal to 8 but ALL face cards are worth 10 and Ace can be used as 11 or 1 it will based on your sum. Lets say you get 2 cards a 9 and a 2 now you have 11 you are givin the option to "hit" or "stand". Hit means you can get another random card now you get a Jack(equals 10) now you have 20 you should stand because if you go over 21 you loose! So when you stand your good with your sum and see if the dealer gets higher. The goal is to try and get the cards equal 21 seems simple right? But can you beat the dealer and make more money? Lets see!
## Notes
- Only one person can play at once
