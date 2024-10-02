import socket 
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *
from filing.file_handling import *


# A thread is needed to receive messages, and the main program itself will be the thread to send them

# Function to continuously receive messages from the client
def receive_messages(conn, private_key):
    while True:
        try:
            # Try to receive data from the client
            data = conn.recv(1024)
            if data:
                msg_c = int.from_bytes(data, byteorder='big')
                msg = decrypt_rsa(msg_c, private_key)
                print(f"\nClient: {msg}")
            else:
                # If no data is received, we can assume the connection is closed
                print("Connection closed by client.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Generate keys
public_key, private_key = generate_rsa_keys()

# Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5656))

server_socket.listen(5) 
conn, addr = server_socket.accept()

##### Keys exchange #### 

# Send public key
file_data = create_json_pbKey(public_key, "server")
conn.sendall(file_data) 

# Receive client key
client_key = receive_json(conn, "server")

print("Connected to the client")

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(conn, private_key))
receive_thread.daemon = True  # The thread will automatically terminate when the main program ends
receive_thread.start()

try:
    while True:
        message = input("You: ")  # Enter a message via the keyboard
        if message.lower() == 'quit':
            break  # Exit the loop if the user types 'quit'
        msg_c = encrypt_rsa(message, client_key)
        # Convert the integer into bytes to send them
        enc_msg_c = msg_c.to_bytes((msg_c.bit_length() + 7) // 8, byteorder='big')
        conn.sendall(enc_msg_c)
except KeyboardInterrupt:
    print("\nServer disconnected.")
finally:
    conn.close()  # Properly close the socket
