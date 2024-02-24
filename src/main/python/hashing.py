import hashlib
import os


def get_hash(name, algorithm='sha256'):
    calculated_hash = hashlib.new(algorithm)
    with open(os.path.join(name), 'rb') as file:
        block = file.read(4096)
        while len(block) > 0:
            calculated_hash.update(block)
            block = file.read(4096)
    return calculated_hash.hexdigest()