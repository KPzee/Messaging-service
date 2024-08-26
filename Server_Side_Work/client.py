# importing the modules needed for server
import socket
import threading

TARGET_HOST = '127.0.0.1'
TARGET_PORT = 1234

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

if __name__ == '__main__':
    main()