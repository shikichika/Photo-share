import hashlib

def make_hash(salt, password):

    dat = salt + password
    hashed_password = hashlib.md5(dat.encode()).hexdigest()

    return hashed_password

