import socket #imports socket to let us run and connect to the server
import time #imports times to give us a slight delay between prompting the client to enter a response
#Start the client
def start_client(): #defines client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Sets up the socket proporties
    client.connect(("127.0.0.1", 5000)) #Connects to the server
    
    while True: #starts a while true loop
        data = client.recv(1024).decode() #if data is sent and recieved by the client its decoded
        if not data: #if there is no data, the code breaks
            break #break
        print(data) #prints the data
        
        if "Goodbye" in data: #if goodbye is in the data, the code break
            break #break
        time.sleep(0.3) #time sleeps for 0.3 seconds
        message = input("Enter your response: ").strip() #asks for an input for the prompt, enter youre response
        client.sendall(message.encode()) #encodes our response and sends it
    
    client.close() #if while loop false, closes the client
    print("Disconnected from server.") #prints disconnected when the client closes

if __name__ == "__main__": #sets main
    start_client() #starts client is called to activate the client
