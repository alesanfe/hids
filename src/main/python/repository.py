import os
import random

from loguru import logger
from neomodel import config, db

from src.main.python.integrity_vertification import get_hash
from src.main.python.models import HashNode

config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'
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

def find_node(root, name):
    print(root, name)
    if root is None:
        return None
    elif root.name == name:
        return root
    elif root.name < name:
        return find_node(root.lower.single(), name)
    else:
        return find_node(root.upper.single(), name)

def add_node_sorted(root, node_list):
    if not node_list:
        return

    mid = len(node_list) // 2
    left_nodes = node_list[:mid]
    right_nodes = node_list[mid+1:]

    add_node(root, node_list[mid])

    add_node_sorted(root, left_nodes)
    add_node_sorted(root, right_nodes)


def add_node(root, new_node):
    if root is None:
        return new_node
    elif root.name > new_node.name:
        son = root.lower.single()
        if son is None:
            root.lower.connect(new_node)
        else:
            add_node(son, new_node)
    else:
        son = root.upper.single()
        if son is None:
            root.upper.connect(new_node)
        else:
            add_node(son, new_node)

if __name__ == '__main__':
    config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'
    db.cypher_query("MATCH(n) DETACH DELETE n")
    load_data()

