import socket 
import threading


#il faut un thread pour recevoir les message et le 
# prog principal est deja un thread qui permettra de les envoyer

# Fonction pour recevoir des messages en continu depuis le client
def receive_messages(conn):
    while True:
        try:
            # On essaie de recevoir des données du serveur
            data = conn.recv(1024)
            if data:
                print(f"\nClient: {data.decode('utf-8')}")
            else:
                # Si aucune donnée reçue, on peut penser que la connexion est fermée
                print("Connection closed by client.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9876))

server_socket.listen(5) 
conn, addr = server_socket.accept()

# Démarrer un thread pour recevoir les messages
receive_thread = threading.Thread(target=receive_messages, args=(conn,))
receive_thread.daemon = True  # Le thread se termine automatiquement lorsque le programme principal se termine
receive_thread.start()

try:
    while True:
        message = input("You: ")  # Entrer un message via le clavier
        if message.lower() == 'quit':
            break  # Quitter la boucle si l'utilisateur tape 'quit'
        conn.sendall(message.encode('utf-8'))  # Envoyer le message au serveur
except KeyboardInterrupt:
    print("\nServer disconnected.")
finally:
    conn.close()  # Fermer le socket proprement
