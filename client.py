import socket #imports socket to let us run and connect to the server
import time #imports times to give us a slight delay between prompting the client to enter a response
#Start the client

def start_client(): #Starts the client 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Connects to the socket
    
    try:
        client.connect(("127.0.0.1", 5000)) #Connects with our network and port
        
        while True: #Use a true loop for if true
            data = client.recv(1024).decode() #When we recieve data we decode it
            if not data: #If we get no data
                raise BrokenPipeError("Server disconnected or stopped") #Raise broken pipe error 
            print(data) #prints data

            time.sleep(0.3) #Waits .3 seconds
            message = input("Enter your response: ").strip() #Displays "Enter your response: " message
            client.sendall(message.encode()) #encodes message back

    except BrokenPipeError: #Excepts broken pipe error if data doesnt come through
        print("Connection to server severed") #Prints "Connection to server severed"
    except KeyboardInterrupt: #When code stopped by keyboard interrupt occurs we do a clean disconnect 
        print("Disconnecting from server") #Prints "Disconnecting from server"        
    except Exception as e: #For anything we don't specify as an error 
        print(f"Client error: {e}") #Prints "Client error: "
    finally: #Using the finally command
        client.close() #Closes the client
        print("Disconnected from server.") #Prints "Disconnected from server."

if __name__ == "__main__": #sets main
    start_client() #starts client is called to activate the client
