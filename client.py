import socket
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *
from filing.file_handling import *


# Function to continuously receive messages from the server
def receive_messages(client_socket, private_key):
    while True:
        try:
            # Try to receive data from the server
            data = client_socket.recv(1024)
            if data:
                msg_c = int.from_bytes(data, byteorder='big')
                msg = decrypt_rsa(msg_c, private_key)
                print(f"\nServer: {msg}")
            else:
                # If no data is received, we can assume the connection is closed
                print("Connection closed by server.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Main function for the client
def client_program():
    ip_server = '127.0.0.1'  # Server address
    port_server = 5656       # Server port

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Generate keys
    public_key, private_key = generate_rsa_keys()

    # Connect to the server
    client_socket.connect((ip_server, port_server))
    print("Connected to the server.")

    ##### Keys exchange ####
    
    # Receive server key
    server_key = receive_json(client_socket, "client")

    # Send public key
    file_data = create_json_pbKey(public_key, "client")
    client_socket.sendall(file_data)
    
    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, private_key,))
    receive_thread.daemon = True  # The thread will terminate automatically when the main program ends
    receive_thread.start()

    # Loop to send messages to the server
    try:
        while True:
            message = input("You: ")  # Enter a message via the keyboard
            if message.lower() == 'quit':
                break  # Exit the loop if the user types 'quit'
            msg_c = encrypt_rsa(message, server_key)
            # Convert the integer into bytes to send them
            enc_msg_c = msg_c.to_bytes((msg_c.bit_length() + 7) // 8, byteorder='big')
            client_socket.sendall(enc_msg_c)  
    except KeyboardInterrupt:
        print("\nClient disconnected.")
    finally:
        client_socket.close()  # Close the socket properly

# Start the client
client_program()
