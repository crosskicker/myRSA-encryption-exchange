import json

def create_json_pbKey(pb_key, name):
    public_key_data = {
        'n': pb_key[0],
        'e': pb_key[1]
    }
    # Write the public key data to a JSON file
    with open('public_key_' + name + '.json', 'w') as f:
        json.dump(public_key_data, f)
    # Read the data back from the file in binary mode
    with open('public_key_' + name + '.json', 'rb') as f:
        file_data = f.read()
    #print("size file : ", len(file_data))
    return file_data

def receive_json(socket, name):
    file_size = 636  # Change if you change the key size RSA-2048 -> 636 ; RSA-4096 -> 1252
    # Receive the file data
    file_data = b""
    while len(file_data) < file_size:
        packet = socket.recv(4096)  # Receive data in blocks of 4096 bytes
        if not packet:
            break
        file_data += packet    
    # Write the received data to a file
    with open('received_' + name + '.json', 'wb') as f:
        f.write(file_data)
    # Read the JSON file and extract the public key values
    with open('received_' + name + '.json', 'r') as f:
        public_key_data = json.load(f)

    n = public_key_data['n']
    e = public_key_data['e']
    public_key = (n, e)
    return public_key
