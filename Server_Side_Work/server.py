# importing the modules needed for server
import socket
import threading

# Here i am defining the constants in the file
HOST = '127.0.0.1'
PORT = 1234
LISTNER_LIMIT = 5
active_clients = [] # list of all currently connected users

# This function will keep listening for new client messages
def listen_for_messages(client, username):
    
    # this while loop will wait to receive message
    while 1:
        response = client.recv(2048).decode('utf-8')
        if response != '':
            final_msg = username + '~' + response 
            send_messages_to_all(messgage=response)
        else:
            print(f'Client response from {username} is empty')

#function to send message to clients
def send_message_to_client(message, client):
    client.sendall(message.encode())

# this message is required by server and when a message is sent, 
# the server will tell every client that this message was sent by this user
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(message=message, client=user[1])


#function to handle client
def client_handler(client):
    
    # Server listening to client for message that will contain username
    while 1:
        # this function is used to listen and receive message from client with a max size of 2048
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            # we break since we have the username already, we don't need the while loop to keep running
            break
        else:
            print('Username is empty')
        
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# This is where the main function begins

def main():
    # Creating the socket class object
    # AF_INET is an IPv4 address family 
    # This is going to be a TCP packet communication defined as SOCK_STREAM
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This is going to try to bind the host to the port and if it fails it will send a failure message to the console
    try:
# Provide the server with address in the form of HOST IP and PORT
        server.bind((HOST, PORT))
        print(f'Running the server on {HOST} {PORT}')
    except:
# This will happen when the server can't bind to the port
        print(f'Unable to bind to {HOST} and port {PORT}')

# Set server limit, don't set to high or it will cause your PC to slow down too much
    else:
        server.listen(LISTNER_LIMIT)   

#This is the while loop that listens to client connections
        while True:

            client, address = server.accept()
            # here adrress[0] is for the Host and address[1] is for the Port
            print(f'Successfully connected to client {address[0]} {address[1]}')

            # we will thread because we don't want the code to only run one function 
            # and stop the while loop
            # this thread will keep running while the client is connected to the server
            threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()