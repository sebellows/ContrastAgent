from sqlalchemy.orm import RelationshipProperty, Mapper


def get_relations(cls):
    mapper = cls if isinstance(cls, Mapper) else cls.__mapper__
    return [c for c in mapper.attrs if isinstance(c, RelationshipProperty)]


def path_to_relations_list(cls, path: str):
    path_as_list = path.split('.')
    relations = get_relations(cls)
    relations_list = []
    for item in path_as_list:
        for rel in relations:
            if rel.key == item:
                relations_list.append(rel)
                relations = get_relations(rel.entity)
                break
    return relations_list