# standard
import json
import logging
import os
import sys
from dataclasses import asdict
# from typing import TYPE_CHECKING

# local
from app.agent.configuration import AppSettings, Config


# if TYPE_CHECKING:
#     from core.models.app_config import AppConfigABC


LOGGER = logging.getLogger(__name__)

def show_only_debug(record):
    return record.levelname != 'INFO'


def show_only_info(record):
    return record.levelname == 'INFO'


class AppConfigBase[T: dict](Config[T]):
    def __init__(self, config=T):
        super().__init__(config)

        env_filepath = config.get('env', None)

        if env_filepath:
            if not os.path.isfile(env_filepath):
                raise ValueError("'.env' file can't be found")
            env_file = open(env_filepath)
            env_data = json.loads(env_file.read())
            self._items = { **config, **env_data }
            self.config_logging()
            LOGGER.debug('Config Initialized')

    def config_logging(self):
        log_level = self.get('LOG_LEVEL', default='DEBUG')
        log_format = self.get('LOG_FORMAT', default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M'
        )
        rootLogger = logging.getLogger()
        
        # Log INFO to stdout
        h1 = logging.StreamHandler(sys.stdout)
        h1.addFilter(show_only_debug)
        rootLogger.addHandler(h1)
        
        # Log not INFO to stderr
        h2 = logging.StreamHandler(sys.stderr)
        h2.addFilter(show_only_info)
        rootLogger.addHandler(h2)


class AppConfig(AppConfigBase):
    def __init__(self, config: dict = None):
        if config is None:
            config = asdict(AppSettings())
        super().__init__(config)
        LOGGER.debug('AppConfig Initialized')


# standard
# from abc import abstractmethod, ABC
# from typing import Any


# class AppConfigABC(ABC):
#     @abstractmethod
#     def items(self):
#         pass
    
#     @abstractmethod
#     def get(self, *paths: tuple[str | list[str]], default=None):
#         pass

#     @abstractmethod
#     def has(self, *paths: tuple[str | list[str]]) -> bool:
#         pass

#     @abstractmethod
#     def get_or_throw(self, path: str | list[str], default=None):
#         pass

#     @abstractmethod
#     def keys(self):
#         pass

#     @abstractmethod
#     def set(self, path: str | list[str], value: Any):
#         pass

#     @abstractmethod
#     def update(self, path: str | list[str], value: Any):
#         pass

#     @abstractmethod
#     def select(self, *paths: tuple[str | list[str]]):
#         pass


# class ApplicationABC(ABC):
#     @property
#     @abstractmethod
#     def fs(self):
#         ...

#     @property
#     @abstractmethod
#     def config(self):
#         ...

#     @property
#     @abstractmethod
#     def state(self):
#         ...

#     @property
#     @abstractmethod
#     def vendor_provider(self):
#         ...

#     @abstractmethod
#     def singleton(
#         self,
#         provider: type[T],
#         to: T | Callable[..., T] | Provider[T] | None = None,
#     ):
#         """
#         Register a shared binding in the app.
#         """
#         ...


# class Application(BaseClass):
#     @property
#     def fs(self):
#         raise NotImplementedError

#     @property
#     def config(self):
#         raise NotImplementedError

#     @property
#     def state(self):
#         raise NotImplementedError

#     @property
#     def vendor_provider(self):
#         raise NotImplementedError

#     def singleton(
#         self,
#         provider: type[T],
#         to: T | Callable[..., T] | Provider[T] | None = None,
#     ):
#         """
#         Register a shared binding in the app.
#         """
#         raise NotImplementedError

#     def register(
#         self,
#         provider: type[T],
#         to: T | Callable[..., T] | Provider[T] | None = None,
#         scope: type["Scope"] | "ScopeDecorator" | None = None,
#     ):
#         raise NotImplementedError

#     @abstractmethod
#     def get_vendor(self, vendor: Any, locale: str, override: Override = Override.NONE):
#         raise NotImplementedError

#     # @abstractmethod
#     # def switch_locale(self, locale: str, override: Override = Override.NONE):
#     #     raise NotImplementedError

#     # @abstractmethod
#     # def switch_vendor(self, vendor: Any, override: Override = Override.NONE):
#     #     raise NotImplementedError

#     # @abstractmethod
#     # def switch_product_line(self, product_line: Any, override: Override = Override.NONE):
#     #     raise NotImplementedError

# ApplicationABC.register(Application)

# AppConfigABC.register(AppConfig)
