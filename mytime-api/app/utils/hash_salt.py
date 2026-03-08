import os
import hashlib
import base64

class HashSalt:
    @staticmethod
    def generate_salted_hash(password: str):
        # Generate a 64-byte random salt (like your C# RNGCryptoServiceProvider)
        salt_bytes = os.urandom(64)
        # Derive the hash using PBKDF2 HMAC SHA1, 10000 iterations, output length 256 bytes
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha1',                     # algorithm (SHA1 to match Rfc2898DeriveBytes default)
            password.encode('utf-8'),   # password bytes
            salt_bytes,                 # salt bytes
            10000,                      # iterations
            dklen=256                   # derived key length in bytes
        )
        # Convert to Base64 for storage (same as C# Convert.ToBase64String)
        salt_b64 = base64.b64encode(salt_bytes).decode('utf-8')
        hash_b64 = base64.b64encode(hash_bytes).decode('utf-8')
        return {"hash": hash_b64, "salt": salt_b64}

    @staticmethod
    def verify_password(entered_password: str, stored_hash: str, stored_salt: str) -> bool:
        # Convert stored salt back to bytes
        salt_bytes = base64.b64decode(stored_salt)
        # Derive hash from entered password using same parameters
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha1',
            entered_password.encode('utf-8'),
            salt_bytes,
            10000,
            dklen=256
        )
        # Convert derived hash to Base64 and compare
        hash_b64 = base64.b64encode(hash_bytes).decode('utf-8')
        return hash_b64 == stored_hash
