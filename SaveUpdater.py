import os

key = 0xF0  # Define the key as an integer

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

def encode_save_file(save_data=False):
    """
    Encodes the Save file in Saves/save.bin
     
    'enchanter':Bool, 'monarch':Bool, 'madman':Bool, 'tutorial':Bool, 'BEFT':Bool
    """
    if not save_data:
        save_data = {
            'enchanter': False,
            'monarch': False,
            'madman': False,
            'tutorial': False,
            'beat_enchanter_first_time': False
        }
        
    # Convert the boolean flags to bytes
    data = bytearray()
    for flag, value in save_data.items():
        data.append(1 if value else 0)
    
    # Encrypt the data
    encrypted_data = xor_encrypt_decrypt(data, key)
    
    # Ensure the Saves directory exists
    saves_dir = os.path.join("Saves")
    os.makedirs(saves_dir, exist_ok=True)
    
    # Write the encrypted data to the file
    save_path = os.path.join(saves_dir, "save.bin")
    with open(save_path, 'wb') as file:
        file.write(encrypted_data)

def decode_save_file():
    """
    Decodes the Save file in Saves/save.bin
    
    'enchanter':Bool, 'monarch':Bool, 'madman':Bool, 'tutorial':Bool, 'BEFT':Bool
    """
    try:
        save_path = os.path.join("Saves", "save.bin")
        with open(save_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        data = xor_encrypt_decrypt(encrypted_data, key)
        
        # Convert the bytes back to boolean flags
        save_data = {
            'enchanter': bool(data[0]),
            'monarch': bool(data[1]),
            'madman': bool(data[2]),
            'tutorial': bool(data[3]),
            'beat_enchanter_first_time': bool(data[4])
        }
        
        return save_data
    except FileNotFoundError:
        print("Save file not found.")
        return None

if __name__ == "__main__":
    save_data = {
        'enchanter': False,
        'monarch': False,
        'madman': False,
        'tutorial': False,
        'beat_enchanter_first_time': False
    }
    encode_save_file(save_data)