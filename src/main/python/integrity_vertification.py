import hashlib
import os

from loguru import logger

from src.main.python.models import HashNode


def get_hash(name, algorithm='sha256'):
    calculated_hash = hashlib.new(algorithm)
    with open(os.path.join(name), 'rb') as file:
        block = file.read(4096)
        while len(block) > 0:
            calculated_hash.update(block)
            block = file.read(4096)
    return calculated_hash.hexdigest()

def check_integrity():
    for node in HashNode.nodes.all():
        if node.hash != "" and node.hash != get_hash(node.path):
            logger.error("File {} has been modified".format(node.path))


