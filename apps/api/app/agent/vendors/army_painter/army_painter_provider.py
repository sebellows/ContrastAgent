from typing import TYPE_CHECKING

from injector import provider, singleton

from app.agent.common_service_provider import CommonServiceProvider

from .army_painter import ArmyPainter


if TYPE_CHECKING:
    from app.agent.providers import IAppConfig, IAppState, FS


class ArmyPainterProvider(CommonServiceProvider):
    # def configure(self, binder: Binder):
    #     super().configure(binder)
    #     binder.bind(ArmyPainter, to=ArmyPainter, scope=singleton)

    @provider
    @singleton
    def provide(self, config: IAppConfig, state: IAppState, fs: FS) -> ArmyPainter:
        return ArmyPainter(config=config, state=state, fs=fs)
