import socket
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *
from filing.file_handling import *


# Fonction pour recevoir des messages en continu depuis le serveur
def receive_messages(client_socket):
    while True:
        try:
            # On essaie de recevoir des données du serveur
            data = client_socket.recv(1024)
            if data:
                print(f"\nServer: {data.decode('utf-8')}")
            else:
                # Si aucune donnée reçue, on peut penser que la connexion est fermée
                print("Connection closed by server.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Fonction principale pour le client
def client_program():
    ip_server = '127.0.0.1'  # Adresse du serveur
    port_server = 5656       # Port du serveur

    # Créer un socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Generate keys
    public_key, private_key = generate_rsa_keys()

    # Connexion au serveur
    client_socket.connect((ip_server, port_server))
    print("Connected to the server.")

    ##### Keys exchange #### 
    
    #receive server key
    server_key = receive_json(client_socket,"client")
    print(server_key)

    #Send public key
    file_data = create_json_pbKey(public_key,"client")
    client_socket.sendall(file_data)
    
    # Démarrer un thread pour recevoir les messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True  # Le thread se termine automatiquement lorsque le programme principal se termine
    receive_thread.start()

    # Boucle pour envoyer des messages au serveur
    try:
        while True:
            message = input("You: ")  # Entrer un message via le clavier
            if message.lower() == 'quit':
                break  # Quitter la boucle si l'utilisateur tape 'quit'
            client_socket.sendall(message.encode('utf-8'))  # Envoyer le message au serveur
    except KeyboardInterrupt:
        print("\nClient disconnected.")
    finally:
        client_socket.close()  # Fermer le socket proprement

# Démarrer le client
client_program()
