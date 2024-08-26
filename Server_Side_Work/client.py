# importing the modules needed for server
import socket
import threading

TARGET_HOST = '127.0.0.1'
TARGET_PORT = 1234

# this is to listen to messages from the server similar to the server code for listening to client
def listen_for_messages_from_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split("~")[1]

            print(f"{username} ~ {content}")
        else:
            print("message from server was empty")

def send_message_to_server(client):
    while True:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Message is empty")
            exit(0)

def communicate_to_server(client):
    # here we are sending the username to the server so it can register it in the client list
    username = input("enter username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print('Username cannot be empty')
        exit(0)
    # we run this as a thread because we want it to keep running so that it can wait for a message
    #  without interfering with the rest of the script
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client=client)

def main():
    # creating a socket object for the client
    # This is the set up as the server because 
    # we want the server and the client to both run on TCP
    #  or else it wont work
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting the client to the server
    try:
        client.connect((TARGET_HOST, TARGET_PORT))
        print('Successfully connected to server')
    except:
        print(f'Unable to connect to server {TARGET_HOST} {TARGET_PORT}')
        exit(0)
    # we don't need a while loop since the client doesn't need to actively listen to the server
    communicate_to_server(client)

if __name__ == '__main__':
    main()