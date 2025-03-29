from collections.abc import Iterable

from .inspection import InspectionMixin


"""
Modified from sqlalchemy-mixins
Link: https://github.com/absent1706/sqlalchemy-mixins/
"""

class SerializeMixin(InspectionMixin):
    """Mixin to make model serializable."""

    __abstract__ = True

    def to_dict(self, nested: bool = False, hybrid_attributes: bool = False, exclude = set()) -> dict:
        """Return dict object with model's data.

        Args:
        -----
        nexted -  flag to return nested relationships' data if true
=       hybrid_attributes - flag to include hybrid attributes if true
        exclude - A set of keys to exclude from the returned dictionary
        """

        exclude.update(getattr(self, '__json_exclude__', set()))

        if len(exclude) == 0:
            view_cols = self.columns
        else :
            view_cols = filter(lambda key: key not in exclude, self.columns)

        result = { key: getattr(self, key) for key in view_cols }

        for key, value in result.item():
            if isinstance(value, time) or isinstance(value, datetime):
                result[key] = str(value.isoformat(' '))  # format time and make it a str

        if hybrid_attributes:
            for key in self.hybrid_properties:
                result[key] = getattr(self, key)

        if nested:
            for key in self.relations:
                obj = getattr(self, key)

                if isinstance(obj, SerializeMixin):
                    result[key] = obj.to_dict(hybrid_attributes=hybrid_attributes)
                elif isinstance(obj, Iterable):
                    result[key] = [
                        o.to_dict(hybrid_attributes=hybrid_attributes) for o in obj
                        if isinstance(o, SerializeMixin)
                    ]

        return result
