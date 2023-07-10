import secrets
import time
import hashlib
import uuid


class KUIDGenerator:
    @staticmethod
    def generate_kuid():
        """Generate a unique, encrypted UUID."""
        timestamp = str(time.time()).encode()
        salt = secrets.token_hex(16).encode()
        kuid = str(uuid.uuid4()) + timestamp.decode()
        salted_kuid = salt + kuid.encode()
        kuid_hash = hashlib.sha3_512(salted_kuid).hexdigest()
        return kuid_hash

    @staticmethod
    def generate_tranid():
        """Generate a unique, encrypted UUID transaction id."""
        timestamp = str(time.time()).encode()
        salt = secrets.token_hex(16).encode()
        tranid = str(uuid.uuid4()) + timestamp.decode()
        salted_tranid = salt + tranid.encode()
        tranid_hash = hashlib.sha3_512(salted_tranid).hexdigest()
        return tranid_hash
