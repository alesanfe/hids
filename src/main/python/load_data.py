import os
import random

from neomodel import db, config

from server import get_hash
from models import HashNode, add_node, add_node_sorted

config.DATABASE_URL = 'bolt://neo4j:ssii1234@localhost:7687'
def load_data():
    for ruta_actual, subcarpetas, archivos in os.walk("../resources"):
        if(ruta_actual=="../resources"):
            continue
        extension_node = HashNode()
        extension_node.name = str(os.path.basename(ruta_actual))
        extension_node.path = str(ruta_actual)
        extension_node.hash = "Sin hash"
        extension_node.save()
        node_list=[]

        for archivo in archivos:
            path = os.path.join(ruta_actual, archivo)
            name=archivo
            hash= get_hash(path)

            new_node = HashNode()
            new_node.name = str(name)
            new_node.path = str(path)
            new_node.hash = str(hash)
            new_node.save()

            node_list.append(new_node)

        add_node_sorted(extension_node,node_list)

if __name__ == "__main__":
    db.cypher_query('MATCH (n:HashNode) DETACH DELETE n')
    load_data()