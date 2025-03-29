# standard
# from typing import TYPE_CHECKING

# packages
from typing import TYPE_CHECKING
from injector import Binder, Module as ServiceProvider, provider, singleton

# local
from .providers import AppConfig, AppState, FilesystemProvider, FS


if TYPE_CHECKING:
    from .providers import FS


class CommonServiceProvider(ServiceProvider):
    def configure(self,binder: Binder):
        binder.bind(AppConfig, to=AppConfig, scope=singleton)
        binder.bind(AppState, to=AppState, scope=singleton)

    @provider
    @singleton
    def provide_fs(self, config: AppConfig, state: AppState) -> FS:
        return FilesystemProvider(config=config, state=state)
