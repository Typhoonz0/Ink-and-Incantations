# SaveUpdater and SaveChecker are the same file
# You can just manually set all values to True before serialising 
# heheheha -liam
import os
import json
import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ---- CONFIG ----
AES_KEY = b"0123456789abcdef0123456789abcdef" # 32 bytes for AES-256
HMAC_SECRET = b"MySuperSecretHMACKey"            # Secret for tamper check
SAVE_FILE_PATH = os.path.join("Saves", "save.bin")

# ---- HELPERS ----
def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt(data_bytes):
    iv = get_random_bytes(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data_bytes))
    return iv + encrypted  # Prepend IV

def decrypt(encrypted_bytes):
    iv = encrypted_bytes[:16]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_bytes[16:])
    return unpad(decrypted)

def compute_hmac(data):
    return hmac.new(HMAC_SECRET, data, hashlib.sha256).digest()

# ---- SAVE/LOAD ----
def encode_save_file(save_data=None):
    if not save_data:
        save_data = {
            'enchanter': True,
            'monarch': True,
            'madman': True,
            'tutorial': True,
            'beat_enchanter_first_time': True,
            'hax': True,
            'i_dont_want_discord': True
        }

    # Serialize to JSON
    json_data = json.dumps(save_data).encode('utf-8')

    # Encrypt it
    encrypted = encrypt(json_data)

    # HMAC the encrypted blob
    hmac_value = compute_hmac(encrypted)

    # Final data = encrypted + hmac
    final_data = encrypted + hmac_value

    # Save to file
    os.makedirs(os.path.dirname(SAVE_FILE_PATH), exist_ok=True)
    with open(SAVE_FILE_PATH, 'wb') as f:
        f.write(final_data)

def decode_save_file():
    try:
        with open(SAVE_FILE_PATH, 'rb') as f:
            content = f.read()

        encrypted_data = content[:-32]
        stored_hmac = content[-32:]

        # Check HMAC
        if compute_hmac(encrypted_data) != stored_hmac:
            raise ValueError("Save file has been tampered with or corrupted.")

        decrypted_json = decrypt(encrypted_data)
        save_data = json.loads(decrypted_json.decode('utf-8'))

        return save_data

    except FileNotFoundError:
        print("Save file not found.")
        return None
    except Exception as e:
        print("Failed to load save:", str(e))
        return None


# ---- DEMO ----
if __name__ == "__main__":
    print("\033[31mC\033[32mh\033[33me\033[34mc\033[35mk\033[36ms\033[37mu\033[38mm \033[0mBypasser")
    print("[\033[31m !! \033[0m] Setting Data...")
    u = True if input(":: Unlock all characters? [Y/n] ") in ("", " ", "y", "Y") else False
    s = True if input(":: Disable music? [Y/n] ") in ("", " ", "y", "Y") else False
    h = True if input(":: Get 10k mana each game? [Y/n] ") in ("", " ", "y", "Y") else False
    vv = True if input(":: Disable RPC? [Y/n] ") in ("", " ", "y", "Y") else False
    t = True if input(":: Disable most fade-in animations? [Y/n] ") in ("", " ", "y", "Y") else False
    data = {
        'enchanter': u,
        'monarch': u,
        'madman': u,
        'tutorial': u,
        'beat_enchanter_first_time': u,
        'shut_up': s, # Disables music 
        '1337_haxxor': h, # Gives lots of mana
        'i_dont_want_discord': vv, # Disables RPC
        'holy_yap': t # Disables general yapping and animations
    }
    encode_save_file(data)
    print("[\033[32m OK \033[0m] Data encoded!")
    decode_save_file()
    print("[\033[32m OK \033[0m] Data decoded!")

