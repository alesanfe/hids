from datetime import datetime

from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, DateProperty, config, db


config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'



class HashNode(StructuredNode):
    name = StringProperty(unique_index=True)
    path = StringProperty(index=True)
    hash = StringProperty(index=True)
    created_at = DateProperty(default=lambda: datetime.now())
    lower = RelationshipTo('HashNode', 'LOWER')
    upper = RelationshipTo('HashNode', 'UPPER')


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


