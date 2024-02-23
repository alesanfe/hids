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
    elif root.name > name:
        return find_node(root.lower.single(), name)
    else:
        return find_node(root.upper.single(), name)


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


if __name__ == "__main__":
    db.cypher_query('MATCH (n:HashNode) DETACH DELETE n')
    a = HashNode()
    a.name = 'a'
    a.path = 'a'
    a.hash = 'a'
    a.size = 'a'
    a.save()

    b = HashNode()
    b.name = 'b'
    b.path = 'b'
    b.hash = 'b'
    b.save()

    c = HashNode()
    c.name = 'c'
    c.path = 'c'
    c.hash = 'c'
    c.save()

    b.lower.connect(a)
    b.upper.connect(c)

    d = HashNode()
    d.name = 'd'
    d.path = 'd'
    d.hash = 'd'
    d.save()

    print(find_node(b, 'a'))
    print(add_node(b, d))
