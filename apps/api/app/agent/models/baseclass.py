from dataclasses import asdict

from pydantic import RootModel, TypeAdapter
from pydantic.dataclasses import dataclass

from app.core.utils.serializer import serialize


@dataclass
class BaseClass:
    """Base Python Dataclass - multipurpose class with custom configuration"""

    @property
    def hash(self) -> int:
        return hash(self.to_json(indent=0))

    def to_dict(self):
        return asdict(self)

    def serialize(self):
        return serialize(asdict(self))

    def to_json(self, **kwargs):
        include = getattr(self.Config, "include", set())
        if len(include) == 0:
            include = None
        exclude = getattr(self.Config, "exclude", set())
        if len(exclude) == 0:
            exclude = None
        return RootModel(self)().model_dump_json(include=include, exclude=exclude, **kwargs)

    @classmethod
    def from_json(cls, data: str):
        """Create a result from a JSON string."""
        return TypeAdapter(cls).validate_json(data)

    @classmethod
    def to_json_schema(cls):
        return TypeAdapter(cls).json_schema()

    @classmethod
    def load(cls, data: dict | str):
        if isinstance(data, str):
            obj = TypeAdapter(cls).validate_json(data)
        else:
            obj = TypeAdapter(cls).validate_python(data)
        return obj

    @classmethod
    def unserialize(cls, data: dict):
        """Unserialize a dictionary into the class instance."""
        return cls(**data)

    class Config:
        pass
