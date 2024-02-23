from datetime import datetime
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, DateProperty, config, db, One, \
    ZeroOrOne

config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'


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

def add_node_sorted(root, node_list):
    if len(node_list) == 1:
        root.lower.connect(node_list[0])
    elif len(node_list) // 2 == 0:
        return None
    else:
        middle = len(node_list) // 2
        left = node_list[:middle]
        right = node_list[middle:]

        root1 = left[-1]
        root2 = right[-1]

        left.remove(root1)
        right.remove(root2)

        root.lower.connect(root1)
        root.upper.connect(root2)

        add_node_sorted(root1, left)
        add_node_sorted(root2, right)


