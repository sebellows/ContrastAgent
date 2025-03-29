from dataclasses import dataclass, field

from .config import Config
from .filesystem import fs_config
from .locales import locales, LocaleDetails
from .vendors import vendor_configs

# app_config = {
#     'app_name': 'Color Agent',
#     'fs': fs_config,
#     'locales': locales,
#     'vendors': vendor_configs,
#     'supported_locales': ['en-US', 'en-GB']
# }

@dataclass
class AppSettings:
    app_name: str = 'Color Agent'
    fs: dict = field(default_factory=dict)
    locales: dict = field(default_factory=dict)
    vendors: dict = field(default_factory=dict)
    supported_locales: list = field(default_factory=list)

    def __post_init__(self):
        self.fs = fs_config
        self.locales = locales
        self.vendors = vendor_configs
        self.supported_locales = ['en-US', 'en-GB']


__all__ = [
    'Config',
    'app_config',
    'locales',
    'LocaleDetails',
]
