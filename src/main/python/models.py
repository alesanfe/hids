from datetime import datetime

from neomodel import StructuredNode, StringProperty, RelationshipTo, DateProperty, ZeroOrOne


class HashNode(StructuredNode):
    name = StringProperty(unique_index=True)
    path = StringProperty(index=True)
    hash = StringProperty(index=True)
    created_at = DateProperty(default=lambda: datetime.now())
    lower = RelationshipTo('HashNode', 'LOWER', cardinality=ZeroOrOne)
    upper = RelationshipTo('HashNode', 'UPPER', cardinality=ZeroOrOne)

