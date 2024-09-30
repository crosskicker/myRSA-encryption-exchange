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
    print("size file : ",len(file_data))
    return file_data

def receive_json(socket, name):
    file_size = 636 #change if you change size key
    # Recevoir les données du fichier
    file_data = b""
    while len(file_data) < file_size:
        packet = socket.recv(4096)  # Recevoir par blocs de 4096 bytes
        if not packet:
            break
        file_data += packet    
    # Écrire les données reçues dans un fichier
    with open('received_'+ name +'.json', 'wb') as f:
        f.write(file_data)
    # Lire le fichier JSON et récupérer les valeurs de la clé publique
    with open('received_'+ name +'.json', 'r') as f:
        public_key_data = json.load(f)

    n = public_key_data['n']
    e = public_key_data['e']
    public_key = (n, e)
    return public_key