# standard
import logging
import os
from typing import TYPE_CHECKING

#packages
from injector import Injector, Module as ServiceProvider, Scope, ScopeDecorator, inject, singleton
from injector import T

# local
from .common_service_provider import CommonServiceProvider
from .vendors import army_painter, games_workshop


if TYPE_CHECKING:
    from .models.vendor import VendorABC as Vendor
    from .providers import IAppConfig, IAppState, FS


logger = logging.getLogger('injector')
logger.setLevel(level=logging.ERROR)

def get_env_tags(tag_list: list[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags

@singleton
@inject
class App:
    _injector: Injector
    
    """Core Providers"""
    _config: IAppConfig
    _state: IAppState
    _fs: FS

    def __init__(
        self,
        config: IAppConfig,
        state: IAppState,
        fs: FS,
        injector: Injector
    ):
        super().__init__()
        self._config = config
        self._state = state
        self._fs = fs
        self._injector = injector

    @classmethod
    def get_instance(cls, providers: list[ServiceProvider]) -> 'App':
        injector = Injector(providers)
        return injector.get(cls)
        
    @property
    def injector(self):
        return self._injector

    @property
    def config(self):
        return self._config

    @property
    def fs(self):
        return self._fs

    @property
    def state(self):
        return self._state

    def get(self, interface: type[T], scope: ScopeDecorator | type[Scope] | None = None) -> T:
        return self.injector.get(interface, scope)

    def get_vendor(self, vendor: Vendor):
        self.state.vendor = vendor
        return self.injector.get(vendor)


def create_app():
    return App.get_instance([CommonServiceProvider, army_painter.ArmyPainterProvider, games_workshop.GamesWorkshopProvider])
