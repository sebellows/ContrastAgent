from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    __abstract__ = True

    """Base for SQLAlchemy declarative models in this project with int primary keys."""

    def to_dict(self):
        json_exclude = getattr(self, '__json_exclude__', set())
        class_dict = {key: value for key, value in self.__dict__.items() if not key.startswith('_')
                      and key not in json_exclude}

        for key, value in class_dict.item():
            if isinstance(value, time) or isinstance(value, datetime):
                class_dict[key] = str(value.isoformat(' '))  # format time and make it a str

        return class_dict

    def to_repr(self, column_names: list[str] = []):
        model_name = self.__class__.name
        column_names.extend(["id", "created_at", "updated_at", "deleted_at", "is_deleted"])
        fields = list(reduce(lambda acc, item: acc if item[0] in column_names else acc += f"{item[0]}={item[1]}", self.__table__.columns.items(), ""))
        return f"{model_name}({', '.join(fields)})"

