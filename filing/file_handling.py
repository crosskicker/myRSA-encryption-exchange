import json

def create_json_pbKey(pb_key,name):
    public_key_data = {
    'n': pb_key[0],
    'e': pb_key[1]
    }
    with open('public_key_'+ name +'.json', 'w') as f:
        json.dump(public_key_data, f)
    with open('public_key_'+ name +'.json', 'rb') as f:
        file_data = f.read()
    print("public key du file server : ",file_data)
    return file_data

def receive_json(socket, name):
    # Recevoir les données du fichier
    print("pret a recevoir")
    file_data = b""
    while True:
        packet = socket.recv(4096)  # Recevoir par blocs de 4096 bytes
        if not packet:
            break
        file_data += packet
    print("j'ai fini de recevoir le fichier")
    
    # Écrire les données reçues dans un fichier
    with open('received_'+ name +'.json', 'wb') as f:
        f.write(file_data)

    print("Fichier reçu et enregistré sous 'received_public_key.json'")

    # Lire le fichier JSON et récupérer les valeurs de la clé publique
    with open('received_'+ name +'.json', 'r') as f:
        public_key_data = json.load(f)

    n = public_key_data['n']
    e = public_key_data['e']
    public_key = (n, e)
    return public_key