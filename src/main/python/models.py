from datetime import datetime
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, DateProperty, config, db, One, \
    ZeroOrOne

class HashNode(StructuredNode):
    name = StringProperty(unique_index=True)
    path = StringProperty(index=True)
    hash = StringProperty(index=True)
    created_at = DateProperty(default=lambda: datetime.now())
    lower = RelationshipTo('HashNode', 'LOWER', cardinality=ZeroOrOne)
    upper = RelationshipTo('HashNode', 'UPPER', cardinality=ZeroOrOne)


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


def add_node(root, new_node):
    if root is None:
        return new_node
    elif root.name < new_node.name:
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

def add_node_sorted(root, lista_nodos):
    if(len(lista_nodos)==1):
        root.lower.connect(lista_nodos[0])
    elif(len(lista_nodos)//2==0):
        None
    else:
        mitad=len(lista_nodos)//2
        izquierda = lista_nodos[:mitad]
        derecha = lista_nodos[mitad:]

        root1=izquierda[-1]
        root2=derecha[-1]

        izquierda.remove(root1)
        derecha.remove(root2)

        root.lower.connect(root1)
        root.upper.connect(root2)

        add_node_sorted(root1,izquierda)
        add_node_sorted(root2,derecha)
