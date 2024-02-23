import hashlib
import os
from loguru import logger

from src.main.python.models import HashNode, add_node_sorted


def load_data():
    for ruta_actual, subcarpetas, archivos in os.walk("../resources"):
        if(ruta_actual=="../resources"):
            continue
        extension_node = HashNode()
        extension_node.name = str(os.path.basename(ruta_actual))
        extension_node.path = str(ruta_actual)
        extension_node.hash = ""
        extension_node.save()
        node_list = []
        for archivo in archivos:
            path = os.path.join(ruta_actual, archivo)
            name=archivo
            # hash= get_hash(path)

            new_node = HashNode()
            new_node.name = str(name)
            new_node.path = str(path)
            new_node.hash = get_hash(path)
            new_node.save()

            node_list.append(new_node)
        add_node_sorted(extension_node,node_list)

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

if __name__ == "__main__":
    check_integrity()

