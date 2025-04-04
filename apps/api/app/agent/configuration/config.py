from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, TypeVar, Dict

# from core.utils.func_utils import get_nested_value, pick_values, set_value, UNDEFINED
import app.core.utils.collection as cu
from app.core.utils.collection.internal import PathT


T = TypeVar("T", bound=Dict)


class ConfigABC(ABC):
    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def get(self, *paths: tuple[str], default=None):
        pass

    @abstractmethod
    def has(self, *paths: tuple[str | list[str]]) -> bool:
        pass

    @abstractmethod
    def get_or_throw(self, path: str | list[str], default=None):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def set(self, path: str | list[str], value: Any):
        pass

    @abstractmethod
    def update(self, path: str | list[str], value: Any):
        pass

    @abstractmethod
    def select(self, *paths: tuple[str | list[str]]):
        pass


class Config[T: dict]:
    _items: T

    def __init__(self, config: T):
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary")
        if not config:
            raise ValueError("Config must not be empty")

        self._items = config

    def items(self):
        return MappingProxyType(self._items)

    def __getitem__(self, item: str):
        return self.get(item)

    def __hasattr__(self, item: str) -> bool:
        return self.has(item)

    def has(self, *paths: PathT) -> bool:
        exists = cu.get_(self._items, *paths, default=None)
        return exists is None

    def get(self, *paths: PathT, default=None):
        return cu.get_(self._items, *paths, default=default)

    def get_or_throw(self, *paths: PathT, default=None):
        try:
            return self.get(*paths, default=default)
        except Exception as e:
            raise (e)

    def keys(self):
        return self._items.keys()

    def set(self, path: PathT, value: Any):
        try:
            cu.set_(self._items, path, value)
        except Exception as e:
            raise (e)

    def update(self, path: str | list[str], value: Any):
        try:
            cu.set_(self._items, path, value)
        except Exception as e:
            raise (e)

    def select(self, *paths: PathT):
        try:
            return cu.pick_values(self._items, paths)
        except KeyError as err:
            raise err
        except Exception as e:
            raise e
