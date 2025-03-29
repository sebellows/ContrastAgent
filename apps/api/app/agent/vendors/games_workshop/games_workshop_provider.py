
from injector import Binder, singleton

from app.agent.common_service_provider import CommonServiceProvider

from .games_workshop import GamesWorkshop

class GamesWorkshopProvider(CommonServiceProvider):
    def configure(self, binder: Binder):
        super().configure(binder)
        binder.bind(GamesWorkshop, to=GamesWorkshop, scope=singleton)
